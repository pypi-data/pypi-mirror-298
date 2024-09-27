from platrock.Common.Objects import GenericRock, GenericCheckpoint, GenericTerrain
from platrock.Common import Utils, Debug, Math, ColorPalettes, BounceModels, ThreeDToolbox
import shapely, quaternion
import numpy as np
from . import RasterTools

import platrock

class Point():
	"""
	A point, which is composing the terrain faces vertex or the rock vertex.
	
	Args:
		id (int): a unique identifier used for the 3D view
		pos (:class:`Common.Math.Vector3` [float,float,float]): absolute x,y,z position components
		vel (:class:`Common.Math.Vector3` [float,float,float]): absolute vx,vy,vz velocity components
		relPos (:class:`Common.Math.Vector3` [float,float,float]): if the point is member of a :class:`Triangulated_Object`, the refPos is the position of the point in the object coordinates (centered at COG).
		VTK_actor (:class:`vtk.VtkActor`): for 3D view
		color (list [1.,0.,0.]): the color of the object for raster or 3D views
		radius (float): the point radius, if any
		TO (:class:`Triangulated_Object`): the triangulated_object the point is member of
		faces (list [:class:`Face`]): the list of all faces the point is member of
	"""
	def __init__(self,x=0,y=0,z=0,TO=None):
		"""
		Constructor:
		
		Args:
			x(float): the x in pos
			y(float): the y in pos
			z(float): the z in pos
		"""
		self.pos=Math.Vector3([x,y,z])
		self.vel=Math.Vector3([0.,0.,0.])
		self.relPos=Math.Vector3([x,y,z])
		self.VTK_actor=None
		self.color=[1.,0.,0.]
		self.radius=0.1
		self.TO=TO
	
	def update_pos(self):
		"""
		Update the position of the point according to its TO attibute.
		"""
		self.pos=quaternion.rotate_vector(self.TO.ori,self.relPos)
		self.pos+=self.TO.pos

class Face():
	"""
	A face, composing a rock or the terrain.
	
	Args:
		id (int): a unique identifier used for the 3D view
		points (:class:`numpy.ndarray` [:class:`Point`,:class:`Point`,:class:`Point`]): an array of 3 points linked by the face
		normal (:class:`Common.Math.Vector3` [float, float, float]): the normal vector of the face
		color (list [1.,0.,0.]): the color of the object for raster or 3D views
		VTK_actor (:class:`vtk.VtkActor`): for 3D view
		TO (:class:`Triangulated_Object`): the triangulated_object the face is member of
		roughness (float): the roughness of the terrain for this face
	"""
	def __init__(self, point1, point2, point3, TO=None, face_params = {}):
		"""
		Args:
			point1 (:class:`Point`): the first point the face is connected to
			point2 (:class:`Point`): the second point the face is connected to
			point3 (:class:`Point`): the third point the face is connected to
		FIXME : DOC
		"""
		self.points=[point1,point2,point3]
		self.normal=None
		self.cog=None
		self.color=[0.68235294, 0.5372549 , 0.39215686]
		self.VTK_actor=None
		self.TO=TO
		self.xyz_bb=None
		
        #Below values and names have already been checked in GenericThreeDTerrain
		for key, value in face_params.items():
			setattr(self, key, value)

		self.xyz_bb=np.array([	min(self.points[0].pos[0],self.points[1].pos[0],self.points[2].pos[0]),
								max(self.points[0].pos[0],self.points[1].pos[0],self.points[2].pos[0]),
								min(self.points[0].pos[1],self.points[1].pos[1],self.points[2].pos[1]),
								max(self.points[0].pos[1],self.points[1].pos[1],self.points[2].pos[1]),
								min(self.points[0].pos[2],self.points[1].pos[2],self.points[2].pos[2]),
								max(self.points[0].pos[2],self.points[1].pos[2],self.points[2].pos[2])])
	
	def is_point_inside_2D(self,point):
		"""
		From an arbitrary point
		"""
		point_xy=point.pos[0:2]	#
		face_points_xy=[p.pos[0:2] for p in self.points ]
		cross_products=[Math.cross2(face_points_xy[i-2]-face_points_xy[i],point_xy-face_points_xy[i]) for i in range(0,3)]
		cross_products_signs_sum=sum(np.sign(cross_products))
		return abs(cross_products_signs_sum)==3
	
	def is_point_inside_3D(self,point):
		"""
		This method is not used anymore. Better do this on 2D ("view from the sky") as it avoids convex edge issues (non detection by the contacts_detector).
		"""
		point_on_face=point.pos - (point.pos-self.points[0].pos).dot(self.normal)*self.normal
		cp1=((self.points[-2].pos-self.points[0].pos).cross(point_on_face-self.points[0].pos)).dot(self.normal)
		cp2=((self.points[-1].pos-self.points[1].pos).cross(point_on_face-self.points[1].pos)).dot(self.normal)
		cp3=((self.points[0].pos-self.points[2].pos).cross(point_on_face-self.points[2].pos)).dot(self.normal)
		#cross_products=[(self.points[i-2].pos-self.points[i].pos).cross(point_on_face-self.points[i].pos) for i in range(0,3)]
		#dots=[cp.dot(self.normal) for cp in cross_products]
		cross_products_signs_sum=np.sign(cp1)+np.sign(cp2)+np.sign(cp3)
		return abs(cross_products_signs_sum)==3
		
			

class Triangulated_Object():
	def __init__(self):
		self.points=np.array([])
		self.faces=np.array([])
		self.VTK_actor=None	#VTK actor for visualization
		self.opacity=1
		self.enable_points_view=False	
		self.points_as_array=np.array([])
	
	def set_points_as_array(self):
		self.points_as_array=np.asarray([p.relPos for p in self.points])


class GenericThreeDRock(GenericRock):
	"""A falling rock."""
	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ori=None

	def setup_kinematics(self, pos=None, vel=None, angVel=None, ori=None):
		self.is_stopped=False
		self.out_of_bounds=False
		self.pos = Math.Vector3(pos)
		self.vel=Math.Vector3(vel)
		self.angVel=Math.Vector3(angVel)
		self.ori=quaternion.from_euler_angles(ori[0],ori[1],ori[2])

class GenericThreeDCheckpoint(GenericCheckpoint):
	def __init__(self,path):
		self.path=np.asarray(path)
	@classmethod
	def _new_retro_compat_template(cls):
		return cls(path=np.asarray([[[0,0],[1,1], [2,2]]])) #same hierarchy as in geojson polylines.
	def init_data(self,simulation):
		"""
		Initialize data lists: :attr:`rocks`, :attr:`heights`, :attr:`vels`, :attr:`angVels`
		"""
		super().init_data()
		self.pos=[]
		self.shapely_linestring=shapely.geometry.LineString(self.path-[simulation.terrain.Z_raster.xllcorner,simulation.terrain.Z_raster.yllcorner])

class Tree(object):
	def __init__(self,pos,dhp=30):
		self.pos = Math.Vector2(pos) #x,y
		self.dhp = dhp
		self.active = True
		self.color = [0,0.8,0]
		self.VTK_actor=None	#VTK actor for visualization

class GenericThreeDTerrain(Triangulated_Object):
	valid_input_soil_geojson_attrs=Utils.ParametersDescriptorsSet([]) #NOTE: must be set in childs

	#NOTE: params_geojson below is deprecated
	def __init__(self,DEM_asc=None,params_geojson=None,soil_params_geojson=None,forest_params_input_file=None, default_faces_params={}):
		Triangulated_Object.__init__(self)
		self.default_faces_params = {}
		self.enable_points_view=False
		self.color=[0.68235294, 0.5372549 , 0.39215686]
		self.trees=[]
		self.trees_as_array=None
		self.vertical_surface=0.
		self.Z_raster=None
		self.opacity=1
		self.soil_params=[]
		self.forest_params=[]
		self.automatic_generate_forest={"enable":False, "density":0, "dhp_mean":0, "dhp_std":0, "mode":"terrain"}
		self._geojson_polygon_soil_offset_applied=False
		self._forest_offset_applied=False

		for param_descriptor in self.valid_input_soil_geojson_attrs.parameters:
			if param_descriptor.inst_name in default_faces_params.keys():
				value = default_faces_params[param_descriptor.inst_name]
			else:
				value = None # will be set to param default value in set_to_obj
			param_descriptor.set_to_obj(self.default_faces_params, value)
        
		if(DEM_asc is not None):
			if(platrock.web_ui):	#don't populate/precompute here, do it in s.before_run_tasks()
				self.set_Z_raster_from_DEM_file(DEM_asc)
			else:	#populate/precompute now 
				self.from_DEM_file(DEM_asc)
		if params_geojson is not None: #retro-compatibility
			soil_params_geojson=params_geojson
		if(soil_params_geojson is not None):
			self.set_soil_params_from_geojson(soil_params_geojson)
		if(forest_params_input_file is not None):
			self.automatic_generate_forest["enable"]=True
			if forest_params_input_file[-8:]==".geojson":
				self.automatic_generate_forest["mode"]="zones"
				self.set_forest_params_from_geojson(forest_params_input_file)
			elif forest_params_input_file[-4:]==".xyd":
				self.automatic_generate_forest["mode"]="xyd"
				self.set_forest_params_from_xyd(forest_params_input_file)

	def from_DEM_file(self,filename):
		self.set_Z_raster_from_DEM_file(filename)
		self.populate_from_Z_raster()
		self.precompute_datas()
	
	"""
	min_value below is a value below which data will be set to None
	"""
	def import_raster_from_DEM_file(self,filename,dest_attr_name,data_name, min_value=None):
		try:
			setattr(self,dest_attr_name,RasterTools.from_asc(filename,data_name,min_value=min_value))
			return 0
		except Exception as e:
			message="Failed to import the Esri grid file:"+str(e)
			Debug.error(message)
			return message

	def set_Z_raster_from_DEM_file(self,filename):
		return self.import_raster_from_DEM_file(filename, 'Z_raster', 'Z')
	
	def set_soil_params_from_geojson(self,params_geojson):
		self._geojson_polygon_soil_offset_applied=False
		return Utils.extract_geojson_to_params_set(params_geojson,self.soil_params,self.valid_input_soil_geojson_attrs,ColorPalettes.qualitative10)
	
	def set_forest_params_from_geojson(self,params_geojson):
		self._forest_offset_applied=False
		return Utils.extract_geojson_to_params_set(params_geojson,self.forest_params,BounceModels.Toe_Tree.valid_input_attrs,ColorPalettes.qualitative10)
	
	def set_forest_params_from_xyd(self,xyd_file):
		try:
			self.forest_params=[] #just to avoid input file collide with webui
			self._forest_offset_applied=False
			with open(xyd_file,'r') as f:
				trees=np.genfromtxt(f,dtype=float,delimiter=",")
			self.automatic_generate_forest["trees_array"]=trees
			self.automatic_generate_forest["mode"]="xyd" #this will disable all automatic generation
			return 0
		except Exception as e:
			message="Failed to import the xyd:"+str(e)
			Debug.error(message)
			return message
		
	def set_faces_params_from_geojson(self):
		#loop on faces to set attrbutes
		for face in self.faces:	#FIXME: this loop can be slow, optimize by replacing shapely "contains" by a cython or numpy array algo ?
			shapely_point=shapely.geometry.Point(face.cog[0:2])
			for soil_param in self.soil_params:
				if(soil_param["shapely_polygon"].contains(shapely_point)):
					face.__dict__.update(soil_param["params"])	#update will overwrite params
					break
	
	def populate_from_Z_raster(self):
			points_ids=np.ones([self.Z_raster.nx,self.Z_raster.ny])*-1 #this is a map of points ids, useful to link [x,y] cells to corresponding point ids.
			#CREATE POINTS :
			nb_points=np.count_nonzero(self.Z_raster.data["Z"]!=self.Z_raster.header_data["NODATA_value"])
			self.points=np.empty(nb_points,dtype=Point)	#to avoid increasing the size of the points array at each new point, instanciate here with the right size.
			counter=0
			for i in range(0,self.Z_raster.nx):
				for j in range(0,self.Z_raster.ny):
					if(not self.Z_raster.data["Z"][i,j]==self.Z_raster.header_data["NODATA_value"]):
						self.points[counter]=Point(self.Z_raster.X[i],self.Z_raster.Y[j],self.Z_raster.data["Z"][i,j])
						points_ids[i,j]=counter
						counter+=1
			# CREATE TRIANGLES :
			# id0---id1
			#  |   / |
			#  |  /  |
			#  | /   |
			# id2---id3
			#to avoid increasing the size of the faces array at each new face, instanciate here.
			#We don't know the exact size now, so use 2*nb_points wich is the worst-case, then finally decrease the size.
			self.faces=np.empty(2*nb_points,dtype=Face)
			counter=0
			for i in range(0,len(self.Z_raster.X)-1):
				for j in range(0,len(self.Z_raster.Y)-1):
					id0=int(points_ids[i,j])
					if(id0!=-1):
						id1=int(points_ids[ i+1 , j   ])
						id2=int(points_ids[ i   , j+1 ])
						id3=int(points_ids[ i+1 , j+1 ])
						if(id1!=-1 and id2!=-1):
							self.faces[counter]=Face(self.points[id0], self.points[id1], self.points[id2],face_params = self.default_faces_params)
							counter+=1
							if(id3!=-1):
								self.faces[counter]=Face( self.points[id1], self.points[id2], self.points[id3],face_params = self.default_faces_params)
								counter+=1
			self.faces=self.faces[0:counter]#clean the array
	
	def set_faces_xyz_bbs(self):
		self.faces_xyz_bb=np.asarray([f.xyz_bb for f in self.faces])

	def set_faces_normals_and_cogs(self):
		ThreeDToolbox.set_faces_normals_and_cogs(self.faces)
			
	def set_vertical_surface(self):
		#compute vertical surface (=surface seen from the sky) :
		self.vertical_surface=0
		for f in self.faces:
			self.vertical_surface += 0.5*np.abs(Math.cross2(f.points[1].pos[0:2]-f.points[0].pos[0:2],f.points[2].pos[0:2]-f.points[0].pos[0:2]))
		self.vertical_surface = float(self.vertical_surface)
	
	def append_tree(self, pos, dhp):
		""" Note: this method is used to instanciate the proper Tree class, it is overriden for instance in ThreeDShape.Objects."""
		self.trees.append(Tree(pos,dhp))

	def generate_random_forest(self,density,dhp_mean,dhp_std):
		self.set_vertical_surface()
		nb_trees=int(density*self.vertical_surface/10000) #NOTE: density is in trees/ha, vertical_surface is in m^2
		nb_faces=len(self.faces)
		self.trees=[]
		for i in range(nb_trees):
			pick_face = self.faces[int(np.random.random()*nb_faces)]
			pt1_xy=pick_face.points[0].pos[0:2]
			pt2_xy=pick_face.points[1].pos[0:2]
			pt3_xy=pick_face.points[2].pos[0:2]
			rand_point = pt1_xy+np.random.random()*(pt2_xy-pt1_xy) # pick a point somewhere between pt1 and pt2
			rand_point = rand_point + np.random.random()*(pt3_xy-rand_point)	# move the previous picked point toward pt3
			dhp = Math.get_random_value_from_gamma_distribution(dhp_mean,dhp_std)
			self.append_tree(pos=rand_point, dhp=dhp)
	
	def generate_forest(self):
		mode=self.automatic_generate_forest["mode"]
		if mode=="terrain": #forest everywhere
			self.generate_random_forest(self.automatic_generate_forest["density"],self.automatic_generate_forest["dhp_mean"],self.automatic_generate_forest["dhp_std"])
		elif mode=="zones":#forest in geojson polygons
			for forest_zone in self.forest_params: #loop on polygons of parameters
				poly=forest_zone["shapely_polygon"]
				minX, minY, maxX, maxY = poly.bounds
				nb_trees=int(forest_zone["params"]["trees_density"]*poly.area/10000) #NOTE: density is in trees/ha, vertical_surface is in m^2
				#basic rejection algorithm:
				t=0
				while t<nb_trees:
					tryX=np.random.random()*(maxX-minX)+minX
					tryY=np.random.random()*(maxY-minY)+minY
					if poly.contains(shapely.geometry.Point(tryX,tryY)):
						dhp = Math.get_random_value_from_gamma_distribution(forest_zone["params"]["trees_dhp_mean"],forest_zone["params"]["trees_dhp_std"])
						self.append_tree(pos=[tryX,tryY], dhp=dhp)
						t+=1
		elif mode=="xyd":#forest in xyd file
			for t in self.automatic_generate_forest["trees_array"]:
				self.append_tree(pos=[t[0],t[1]], dhp=t[2])

	def precompute_datas(self):
		self.set_faces_normals_and_cogs()
		self.set_points_as_array()
		self.set_faces_xyz_bbs()
		self.min_height=self.points_as_array[:,2].min()