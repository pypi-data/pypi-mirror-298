"""
This module is used by the ThreeDShape model. It handles all the Objects types
"""

from platrock.Common.ThreeDObjects import GenericThreeDRock, Triangulated_Object, Point, Face, GenericThreeDTerrain, GenericThreeDCheckpoint
from platrock.Common import BounceModels, Utils, Math, Debug
from platrock.Common.ThreeDObjects import Tree as ThreeDTree
from siconos.mechanics.collision.convexhull import ConvexHull
from traceback import format_exc

import numpy as np
from stl import mesh as stlmesh
import locale, os, re

class Rock(GenericThreeDRock, Triangulated_Object):
	valid_shape_params=Utils.ParametersDescriptorsSet([
	])
	@classmethod
	def get_subclasses_names(cls):
		return [klass.__name__ for klass in cls.__subclasses__()]
	
	@classmethod
	def get_subclass_from_name(cls, name):
		name = name.lower()
		subclasses = cls.__subclasses__()
		subclasses_names = [klass.__name__.lower() for klass in cls.__subclasses__()]
		if name not in subclasses_names:
			return False
		return subclasses[subclasses_names.index(name)]

	def __init__(self,**kwargs):
		# SET THE ROCKS DEFAULT PARAMS :
		for p in self.valid_shape_params.parameters:
			p.set_to_obj(self)
		# Override the defaults params with the given kwargs
		for key in kwargs.keys():
			param_descriptor=self.valid_shape_params.get_param_by_input_name(key)
			if(param_descriptor):
				param_descriptor.set_to_obj(self,kwargs[key])
		GenericThreeDRock.__init__(self, density=1, volume=1) #density and volume are just here to avoid Common.Objects to crash. Values will be overriden later.
		self._base_vertices=None
		self._base_inertia=None #inertia corresponding to a volume of 1 and a density of 1
		self._initial_volume=None #this is the volume of the rock before its shape normalisation. Only used by WebUI with PointsList type.
		self.vertices=None
		self._siconos_convex_hull=None

		Triangulated_Object.__init__(self)
	
	def vertices_to_string(self, points=None):
		if points is None:
			points = self.vertices
		if points is None:
			return None
		s=''
		for v in points:
			s+=' '.join(v.astype(str))
			s+='\n'
		return s
	
	def get_unique_edges_ids(self):
		l=[]
		for face_pts in self._siconos_convex_hull.hull.vertices:
			for i,j in [[0,1],[0,2],[1,2]]:
				pt0 = min(face_pts[i], face_pts[j])
				pt1 = max(face_pts[i], face_pts[j])
				l.append([pt0,pt1])
		l=np.asarray(l)
		return np.unique(l,axis=0)
	
	def get_unique_edges_coords(self):
		pts_ids = self.get_unique_edges_ids()
		return self.vertices[pts_ids]
		
	"""
	This method is called right after shape vertex definition. Its goal is to modify the shape so that it fits PlatRock convention :
	- the shape must be convex
	- the corresponding polygon COG must be at (0,0)
	- the polygon volume must be ==1
	- the _base_inertia is computed, for volume=1 and density=1 
	"""
	def __normalize_shape__(self):
		self._base_vertices = np.array(self._base_vertices)
		# NOTE: the following line is a workaround for a bug that appears when using the 3DView. For some reason, an import in the 3D view sets the numeric locale to the system locale. After that qhull waits for the locale decimal separator, but pyhull always gives '.' as the decimal separator. It makes qhull to fail for instance with french system locals.
		locale.setlocale(locale.LC_NUMERIC,'C')
		self._siconos_convex_hull = ConvexHull(self._base_vertices)
		phch = self._siconos_convex_hull.hull # "PyHull Convex Hull"
		#1- Cleanup vertices (= remove concave points):
			#NOTE: phch.vertices are not really vertices, but rather a list of index of points (into self._base_vertices) that forms the faces of the convex shell : [[i_face1_pt1, i_face1_pt2, i_face3_pt3], [i_face2_pt1, i_face2_pt2, i_face2_pt3], ...]
			#So using numpy "flatten" then "unique" is a way to select only the points into self._base_vertices that are involved in the convex shell (concave points are filtered out).
		self._base_vertices = phch.points[np.sort(np.unique(np.array(phch.vertices).flatten()))]

		if (hasattr(self, 'y_aspect_ratio') and hasattr(self, 'z_aspect_ratio')): #NOTE: PointsList don't have aspect ratios
			#2- transform the shape to fit y_aspect_ratio and z_aspect_ratio:
			#	2.1- transform x coordinates to exactly fit [0, 1] interval.
			self._base_vertices[:,0] -= self._base_vertices[:,0].min()
			self._base_vertices[:,0] /= self._base_vertices[:,0].max()
			#	2.2- transform y coordinates to exactly fit [0, y_aspect_ratio] interval.
			self._base_vertices[:,1] -= self._base_vertices[:,1].min()
			self._base_vertices[:,1] /= self._base_vertices[:,1].max()
			self._base_vertices[:,1] *= self.y_aspect_ratio
			#	2.3- transform z coordinates to exactly fit [0, z_aspect_ratio] interval.
			self._base_vertices[:,2] -= self._base_vertices[:,2].min()
			self._base_vertices[:,2] /= self._base_vertices[:,2].max()
			self._base_vertices[:,2] *= self.z_aspect_ratio
		self._siconos_convex_hull = ConvexHull(self._base_vertices)#new convex hull, cleaned and with correct aspect ratio.

		#3- Move the shape center of mass to origin [0, 0, 0]:
		self._base_vertices -= self._siconos_convex_hull.centroid()
		self._siconos_convex_hull = ConvexHull(self._base_vertices)#center the shape
		#NOTE: reset the locale below to avoid issues with other libs.
		locale.setlocale(locale.LC_NUMERIC,'')

		#4- The following line normalizes the __base volume (V:=1) and the density (=1), then computes everything for the __base solid
		self.set_volume(1.,modify_base_shape=True)
	
	"""
	Homothetic transform of the rock, with modification of all geometrical and physical quantities
	It uses the __base*__ normalized solid to fastly apply the changes, so only set modify_base_shape to True at rock instanciation for normalization purpose.
	"""
	def set_volume(self,dest_vol,modify_base_shape=False):
		if modify_base_shape: #only at rock instanciation
			self._base_inertia, start_volume = self._siconos_convex_hull.inertia([0., 0., 0.]) #assume density:=1 for now, so inertia will be recomputed later as it is proportionnal to density
			self._initial_volume=start_volume
		else:
			start_volume=1# normally after instanciation the __base volume is 1
		vol_factor=dest_vol/start_volume
		coord_factor=vol_factor**(1/3)
		if modify_base_shape: #this will be run at instanciation
			self._base_vertices*=coord_factor # homothetic transform -> now vol==1
			self._base_inertia*=coord_factor**5 # base inertia for vol==1 and density ==1
		else: # this will be run before rock launch
			self.volume=dest_vol
			self.vertices=self._base_vertices*coord_factor
			self.I=self._base_inertia*coord_factor**5*self.density
			self.mass=self.volume*self.density
			self.dims = [	self.vertices[:,0].max() - self.vertices[:,0].min(),
							self.vertices[:,1].max() - self.vertices[:,1].min(),
							self.vertices[:,2].max() - self.vertices[:,2].min()]
			self.radius = (3/4*self.volume/np.pi)**(1/3) #equivalent sphere radius
	
	# for compatibility with 3D view :
	def generate_TO_points_faces(self):
		self.points=[]
		self.faces=[]
		for p in self.vertices:
			self.points.append(Point(p[0],p[1],p[2],TO=self))
		self.points = np.asarray(self.points)
		for [i,j,k] in self._siconos_convex_hull.hull.vertices:
			self.faces.append(
				Face(
					self.points[i],
					self.points[j],
					self.points[k],
					TO=self
				)
			)

class Parallelepiped(Rock):
	valid_shape_params=Rock.valid_shape_params+Utils.ParametersDescriptorsSet([
		[["rocks_y_aspect_ratio", "y_aspect_ratio"],	"y_aspect_ratio",	"Aspect ratio along y",	float,	1,	10,	2],
		[["rocks_z_aspect_ratio", "z_aspect_ratio"],	"z_aspect_ratio",	"Aspect ratio along z",	float,	1,	10,	1]
	])
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self._base_vertices= np.array([
			[0.,0.,0.],
			[0.,0.,1],
			[0.,1,1],
			[0.,1,0.],
			[1.,0.,0.],
			[1.,0.,1],
			[1.,1,1],
			[1.,1,0.]
		])
		self.__normalize_shape__()

class Random(Rock):
	valid_shape_params=Parallelepiped.valid_shape_params+Utils.ParametersDescriptorsSet([
		[["rocks_nbPts", "nbPts"],	"nbPts",	"Number of points",	int,4,50,10],
		[["rocks_nb_diff_shapes", "nb_diff_shapes"],	"nb_diff_shapes",	"Number of different shapes",	int, 1, 10000, 1]
	])
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.generate()
	
	def generate(self):
		#NOTE: generate way too much points as pyhull (qhull) will have to ignore a lot of them to get a CONVEX hull. So at first we don't have a good control on nbPts...
		self._base_vertices= np.random.rand(self.nbPts*100,3)
		self.__normalize_shape__()
		#NOTE: after __normalize_shape__, the shape is now convex, but we don't respect self.nbPts vertices, we hope to have more so we just have to remove some of them.
		nb_points_to_remove = len(self._base_vertices) - self.nbPts
		if nb_points_to_remove < 0:
			Debug.error('In random shape generation, nb_points_to_remove was negative:',nb_points_to_remove)
			return
		for i in range(nb_points_to_remove):
			del_index = np.random.randint(self._base_vertices.shape[0])
			self._base_vertices = np.delete(self._base_vertices, del_index, axis=0)
		# renormalize shape as we likely changed its volume and size above.
		self.__normalize_shape__()

class PointsList(Rock):

	valid_shape_params=Rock.valid_shape_params+Utils.ParametersDescriptorsSet([
		["FreeString", "rocks_pointslist_string",	"rocks_pointslist_string",	"Rocks input vertex\nA series of {xi, yi, zi} coordinates in csv format (one vertex per line, three coordinates per line). Note that the resulting polygon must be concave, otherwise it will be silently converted.",	"", "x0 y0 z0\nx1 y1 z1\n..."]
	])

	@classmethod
	def _new_retro_compat_template(cls):
		return cls(rocks_pointslist_string='0. 0. 0. \n 0.5 0. 0. \n 0. 0.5 0. \n 0.25 0.25 0.5')

	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self._base_vertices = PointsList.input_string_to_points(self.rocks_pointslist_string)
		assert self._base_vertices is not False
		self.__input_vertices__ = self._base_vertices.copy()
		self.__normalize_shape__()
		
	@staticmethod
	def validate_points(points):
		if(len(points)<4 or points.shape[1]!=3):
			return False
		return True
	
	@staticmethod
	def input_string_to_points(input_str):
		"""
		NOTE: input_str can be an xyz filepath, an stl filepath, or a string representing the content of an xyz file.
		"""
		if (os.path.isfile(input_str)):
			Debug.info('The input str is a filepath')
			try:
				points = PointsList.stl_file_to_points(input_str)
				assert PointsList.validate_points(points)
				return points
			except Exception:
				Debug.info('The input was not a valid stl file. The error was: '+format_exc())
			try:
				with open(input_str, 'r') as f:
					input_str = f.read()
			except Exception:
				Debug.warning('Unable to read the input file.')
		try:
			points = PointsList.xyz_string_to_points(input_str)
			assert PointsList.validate_points(points)
			return points
		except Exception:
			Debug.error('Unable to load a rock from the input_str='+input_str+'. The error was: '+format_exc())
			return False
	
	@staticmethod
	def stl_file_to_points(file):
		mesh = stlmesh.Mesh.from_file(file)
		points = np.unique(mesh.points.reshape(int(np.size(mesh)/3),3),axis=0)
		return points

	@staticmethod
	def xyz_string_to_points(string):
		lines = string.split('\n')
		points=[]
		#NOTE: regex inpired from https://stackoverflow.com/questions/14550526/regex-for-both-integer-and-float
		numbers_regex = re.compile(r'([+-]?([0-9]+)(\.([0-9]+))?)([eE][+-]?\d+)?')
		for line in lines:
			try:
				matches = [it.group() for it in re.finditer(numbers_regex, line)]
				xyz = np.asarray(matches, dtype=float)
				assert(len(xyz)==3)
				points.append(xyz)
			except Exception as e:
				Debug.warning("Invalid input xyz line \""+str(line).replace('\n','\\n')+'". It was omitted.')
				continue
		return np.asarray(points)

class Tree(ThreeDTree):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._siconos_collision_group = None
		self._siconos_translation = None
		self._siconos_orientation = None
		self._siconos_static_body_number = None #for siconos + tree removal

class Terrain(GenericThreeDTerrain):
	valid_input_soil_geojson_attrs = \
		Utils.ParametersDescriptorsSet([
			BounceModels.BounceModel.valid_input_attrs.get_param_by_instance_name("mu_r")
		]) + \
		Utils.ParametersDescriptorsSet([
			["e",		"e",		"e",	float,	0,	1,		0.1],
			["mu",		"mu",		"μ",	float,	0,	100,	0.2],
		])
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)	
		self._siconos_trees_ids_to_tree_id = {}
	
	def append_tree(self, pos, dhp):
		self.trees.append(Tree(pos,dhp))

class Checkpoint(GenericThreeDCheckpoint):
	pass #nothing to change to the parent class, just declare here for consistency and facilitate eventual future implementations.