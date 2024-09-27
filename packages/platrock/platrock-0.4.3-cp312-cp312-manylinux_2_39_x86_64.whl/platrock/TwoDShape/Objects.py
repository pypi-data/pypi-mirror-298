"""
"""

import numpy as np
import io, os, re
from platrock.Common.TwoDObjects import GenericTwoDRock, GenericSegment, GenericTwoDCheckpoint, GenericTwoDTerrain
import platrock.Common.BounceModels as BounceModels
import platrock.Common.Utils as Utils
import platrock.Common.Math as Math
import platrock.Common.Debug as Debug
from traceback import format_exc

class Rock(GenericTwoDRock):
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
		super().__init__(density=1.0, volume=1.0) #density and volume are just here to avoid Common.Objects to crash. Values will be overriden later.
		self._base_vertices=None #inertia corresponding to a volume of 1 once _base_ly is set
		self._base_inertia=None #inertia corresponding to a volume of 1 and a density of 1
		self._base_ly=None #the third dimension, equal to the dimension in the Z axis for a volume of 1
		self._initial_volume=None #this is the volume of the rock before its shape normalisation. Only used by WebUI with PointsList type.
		self.vertices=None
		self.ly=None
		
	"""
	This method is called right after shape vertex definition. Its goal is to modify the shape so that it fits PlatRock convention :
	- the _base_vertices must be sorted in polar coord system (use Math.sort_2d_polygon_vertices)
	- the corresponding polygon COG must be at (0,0) (use Math.center_2d_polygon_vertices)
	- the polygon volume must be ==1
	- the _base_inertia is computed for volume=1 and density=1
	"""
	def __normalize_shape__(self):
		#Cleanup vertices:
		Math.sort_2d_polygon_vertices(self._base_vertices)
		Math.center_2d_polygon_vertices(self._base_vertices)
		#The following line normalizes the __base volume (V==1) and the density (=1), then computes everything for the __base solid
		self.set_volume(1.,modify_base_shape=True)
	
	"""
	Homothetic transform of the rock, with modification of all geometrical and physical quantities
	It uses the __base*__ normalized solid to fastly apply the changes, so only set modify_base_shape to True at rock instanciation for normalization purpose.
	"""
	def set_volume(self,dest_vol,modify_base_shape=False):
		if modify_base_shape: #only at rock instanciation
			start_area,self._base_inertia = Math.get_2D_polygon_area_inertia(self._base_vertices,1.,cog_centered=True) #assume 2D density=1 for now, so inertia will be computed later as it is proportionnal to density
			self._base_inertia*=self._base_ly #now we switch to 3D density=1
			start_volume=start_area*self._base_ly
			self._initial_volume=start_volume
		else:
			start_volume=1# normally after instanciation the __base volume is 1
		vol_factor=dest_vol/start_volume
		coord_factor=vol_factor**(1/3)
		if modify_base_shape: #this will be run at instanciation
			self._base_vertices*=coord_factor
			self._base_ly*=coord_factor
			self._base_inertia*=coord_factor**5
		else: # this will be run before rock launch
			self.volume=dest_vol
			self.vertices=self._base_vertices*coord_factor
			self.points_as_array = self.vertices # for compatibility with ThreeD's TriangulatedObject.
			self.ly=self._base_ly*coord_factor
			self.I=self._base_inertia*coord_factor**5*self.density
			self.mass=self.volume*self.density
			self.dims = [	self.vertices[:,0].max() - self.vertices[:,0].min(),
							self.vertices[:,1].max() - self.vertices[:,1].min()]
			self.radius = (3/4*self.volume/np.pi)**(1/3) #NOTE: equivalent sphere radius
	
	def setup_kinematics(self, ori=None, **kwargs):
		super().setup_kinematics(**kwargs)
		self.ori = ori
	
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

"""
NOTE: in all the shapes below, the output (=self._base_vertices) is supposed to be a list of vertices with the following characteristics:
- the larger dimension must be along X (for aspect_ratio > 1)
- the polygon formed 
"""
class Rectangle(Rock):
	valid_shape_params=Utils.ParametersDescriptorsSet([
		["aspect_ratio",	"aspect_ratio",	"Aspect ratio",	float,	1,	10,	2]
	])
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		#Start with a rectangle of size along x == 1, centered at (0,0)
		Lx=1
		Lz=Lx/self.aspect_ratio
		self._base_vertices=np.array([[-Lx/2, -Lz/2], [Lx/2, -Lz/2], [Lx/2, Lz/2], [-Lx/2, Lz/2]])
		#Set the last (virtual) dimension to the smallest one (so the one along Z)
		self._base_ly=Lz
		self.__normalize_shape__()

class Ellipse(Rock):
	valid_shape_params=Rectangle.valid_shape_params+Utils.ParametersDescriptorsSet([
		["nbPts",	"nbPts",	"Number of points",	int,3,100,10]
	])
	def __init__(self,**kwargs):
		super(Ellipse,self).__init__(**kwargs)
		Lx=1
		Lz=Lx/self.aspect_ratio
		t=np.linspace(0,np.pi*2,self.nbPts+1)[:-1]
		self._base_vertices=np.array([Lx/2.*np.cos(t) , Lz/2.*np.sin(t)]).transpose()
		self._base_ly=self._base_vertices[:,1].max()-self._base_vertices[:,1].min()
		self.__normalize_shape__()

class Random(Rock):
	valid_shape_params=Ellipse.valid_shape_params+Utils.ParametersDescriptorsSet([
		["nb_diff_shapes",	"nb_diff_shapes",	"Number of different shapes",	int,1,10000,1]
	])
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.generate()
	def generate(self):
		Lx=1
		Lz=Lx/self.aspect_ratio
		self._base_vertices=Math.get_random_convex_polygon(self.nbPts,Lx,Lz)
		self._base_ly=Lz
		self.__normalize_shape__()

class PointsList(Rock):

	valid_shape_params=Rock.valid_shape_params+Utils.ParametersDescriptorsSet([
		["FreeString", "rocks_pointslist_string",	"rocks_pointslist_string",	"Rocks input vertex\nA series of {xi, yi} coordinates in csv format (one vertex per line, two coordinates per line). Note that the resulting polygon must be concave, otherwise it will be silently converted.",	"", "x0 y0\nx1 y1\n..."]
	])

	@classmethod
	def _new_retro_compat_template(cls):
		return cls(rocks_pointslist_string='0. 0. \n 1. 0. \n 0. 1.')

	def __init__(self, points=None, **kwargs):
		super().__init__(**kwargs)
		if (points is not None):
			self._base_vertices = points
		else:
			self._base_vertices = PointsList.input_string_to_points(self.rocks_pointslist_string)
		assert self._base_vertices is not False
		self.__input_vertices__ = self._base_vertices.copy()
		self._base_ly=self.get_secondary_axis_extents(self._base_vertices)
		self.__normalize_shape__()
	
	@staticmethod
	def validate_points(points):
		if (len(points)<3 or points.shape[1]!=2):
			return False
		if (PointsList.points_are_convex(points)):
			return True
		return False
	
	@staticmethod
	def input_string_to_points(input_str):
		"""
		NOTE: input_str can be an xy filepath or a string representing the content of an xy file.
		"""
		if (os.path.isfile(input_str)):
			Debug.info('The input str is a filepath')
			try:
				with open(input_str, 'r') as f:
					input_str = f.read()
			except Exception:
				Debug.warning('Unable to read the input file.')
		try:
			points = PointsList.xy_string_to_points(input_str)
			Math.sort_2d_polygon_vertices(points)
			assert PointsList.validate_points(points)
			return points
		except Exception:
			Debug.error('Unable to load a rock from the input_str='+input_str+'. The error was: '+format_exc())
			return False
	
	@staticmethod
	def xy_string_to_points(string):
		lines = string.split('\n')
		points=[]
		#NOTE: regex inpired from https://stackoverflow.com/questions/14550526/regex-for-both-integer-and-float
		numbers_regex = re.compile(r'([+-]?([0-9]+)(\.([0-9]+))?)([eE][+-]?\d+)?')
		for line in lines:
			try:
				matches = [it.group() for it in re.finditer(numbers_regex, line)]
				xy = np.asarray(matches, dtype=float)
				assert(len(xy)==2)
				points.append(xy)
			except Exception as e:
				Debug.warning("Invalid input xy line \""+str(line).replace('\n','\\n')+'". It was omitted.')
				continue
		return np.asarray(points)

	@classmethod
	def new_from_points(cls, points):
		try:
			Math.sort_2d_polygon_vertices(points)
			assert PointsList.validate_points(points)
			return cls(points=points)
		except Exception:
			Debug.error('Unable to valide input points array. The error was: '+format_exc())
			return False
	
	@staticmethod
	def get_secondary_axis_extents(points):
		points = np.copy(points)
		n=len(points)
		#Find the largest point-point distance:
		maxDist=-np.inf
		id1=-1 ; id2=-1
		for i in range(n):
			for j in range(i+1,n):
				d=Math.Vector2(points[i]-points[j]).norm()
				if(d>maxDist):
					maxDist=d
					id1=i ; id2=j
		#Find the angle of the largest point-point distance:
		long_vect = points[id1]-points[id2]
		angle = - np.arctan2(long_vect[1],long_vect[0])
		#Rotate the polygon to align its principal axis with X
		Math.rotate_points_around_origin(points,angle)
		return points[:,1].max()-points[:,1].min()

	@staticmethod
	def points_are_convex(points):
		points_0shift = points
		points_1shift = np.roll(points,shift=1,axis=0) # "points shifted by 1"
		points_2shift = np.roll(points,shift=2,axis=0) # "points shifted by 1"
		cross_prods = np.cross(points_0shift-points_1shift, points_2shift-points_1shift)
		signs = np.sign(cross_prods)
		if((signs==1).all() or (signs==-1).all()): #all cross products have the same sign: its a convex polygon
			return True
		return False


class Segment(GenericSegment):
	valid_input_attrs = \
		Utils.ParametersDescriptorsSet([
			BounceModels.BounceModel.valid_input_attrs.get_param_by_instance_name("mu_r")
		]) + \
		Utils.ParametersDescriptorsSet([
			["e",		"e",		"e",	float,	0,	1,		0.1],
			["mu",		"mu",		"μ",	float,	0,	100,	0.2],
		])
	valid_input_attrs+=BounceModels.Toe_Tree.valid_input_attrs

class Checkpoint(GenericTwoDCheckpoint):
	pass #nothing to change to the parent class, just declare here for consistency and facilitate eventual future implementations.

class Terrain(GenericTwoDTerrain):
	valid_input_attrs=Segment.valid_input_attrs


