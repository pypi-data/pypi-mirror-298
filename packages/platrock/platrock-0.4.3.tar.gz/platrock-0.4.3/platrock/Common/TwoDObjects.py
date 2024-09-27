from platrock.Common.Objects import GenericRock, GenericCheckpoint, GenericTerrain
from platrock.Common.Utils import ParametersDescriptorsSet
from platrock.Common import Math, PyUtils, ColorPalettes, Debug
from platrock.TwoD import Geoms
import numpy as np
import math, copy

class GenericTwoDRock(GenericRock):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.current_segment=None
		self.flying_direction=0

	def setup_kinematics(self,x=None,height=None,vel=None,angVel=None):
		"""
		Set the rock kinematics quantities, such as velocity and position.
		
		Args:
			x (float): see :class:`Rock` constructor.
			height (float): see :class:`Rock` constructor.
			vel (:class:`~platrock.Common.Math.Vector2` [float,float]): see :class:`Rock` constructor.
			angVel (float):  see :class:`Rock` constructor.
		"""
		self.pos=Math.Vector2([x,height])
		self.vel=Math.Vector2(vel)
		self.angVel=Math.Vector1(angVel)
		self.is_stopped=False
		self.current_segment=None
		self.flying_direction=0
		self.out_of_bounds=False

	def update_current_segment(self,input):
		"""
		Update the :attr:`current_segment` of this rock.
		
		Args:
			input (:class:`GenericSegment` || :class:`GenericTerrain`): the new segment directly or the terrain from which to compute it.
		"""
		if(isinstance(input,GenericSegment)):
			self.current_segment=input
			Debug.info("CURRENT SEGMENT IS SET TO N",self.current_segment.index)
		elif(isinstance(input,GenericTwoDTerrain)):
			terrain_points=input.get_points()
			seg=input.segments[np.where(terrain_points[:,0]<=self.pos[0])[0][-1]]
			if abs(self.pos[0]-seg.points[0][0]) < 1e-10: #we are exactly at a point, use velocity to choose between segment before or after.
				self.current_segment = seg if self.flying_direction>0 else input.segments[seg.index-1]
			else :
				self.current_segment=seg
			Debug.info("CURRENT SEGMENT IS SET TO N",self.current_segment.index)
		else:
			Debug.info("ERROR, update_current_segment_number called with a wrong input parameter.")

class GenericSegment(object):
	"""
	A segment of the terrain. Attributes from all bounce models / rolls will be considered as valid, they are stored in :attr:`valid_input_attrs`, with values : :pyDocPrint:`valid_input_attrs`
	
	Args:
		start_point (:class:`~platrock.Common.Math.Vector2`): start point coordinates of the segment (:math:`[x_{start}, z_{start}]`)
		end_point (:class:`~platrock.Common.Math.Vector2`): end point coordinates of the segment (:math:`[x_{end}, z_{end}]`)
		
	Attributes:
		points (np.ndarray): start and end points in the form :math:`[ [x_{start}, z_{start}], [x_{end}, z_{end}] ]`
		index (int): index of the segment (they are continuously and automatically indexed through the terrain)
		branch (:class:`~platrock.Common.Math.Vector2`): the vector connecting :attr:`start_point` to :attr:`end_point`
		normal (:class:`~platrock.Common.Math.Vector2`): the segment normal vector
		slope_gradient (float): the gradient of slope (:math:`\\Delta_z / \\Delta_x`)
		slope (float): the slope in radians, CCW
	"""
	
	valid_input_attrs=ParametersDescriptorsSet([]) # set in subclasses
	
	def __init__(self, start_point, end_point):
		self.points=np.array([start_point,end_point])
		# SET THE DEFAULT PARAMS :
		for p in self.valid_input_attrs.parameters:
			p.set_to_obj(self)
		self.index=-1
		self.set_geometrical_quantities()
	
	@classmethod
	def _new_retro_compat_template(cls):
		return cls([0, 0],[10, 15])
	
	def set_geometrical_quantities(self):
		"""
		Sets the branch, slopes, normal from the input segment points. Useful at segment init then when a point is moved along the terrain profile.
		"""
		self.branch=Math.Vector2(self.points[1]-self.points[0])
		if(abs(self.branch[0])<1e-5):
			self.slope_gradient=0.
		else:
			self.slope_gradient=self.branch[1]/self.branch[0]
		self.normal=self.branch.rotated(np.pi/2.).normalized()
		self.slope=np.arctan(self.slope_gradient)
	
	def get_z(self,x):
		"""
		Get the y value from a x value. Warning, x must be between segment start and end.
		
		Args:
			x (float)
		
		Returns:
			z (float)
		"""
		return self.points[0][1]+self.slope_gradient*(x-self.points[0][0])
PyUtils.pyDocPrint(GenericSegment)

class TwoDParamsDict(dict): #subclass dict to be able to i)put attributes (with ".") on a dict ; and ii) propagate params to segments on key assignation (with "[]").
	def __init__(self,zone,terrain):
		super().__init__()
		self.zone=zone
		for attr in terrain.valid_input_attrs.get_instance_names(): #import parameters from start_id
			super().__setitem__(attr, self.zone.segments[self.zone.start_id].__dict__[attr]) #use "super" to avoid the usage of __setitem__ below.

	def __setitem__(self,item,value):
		super().__setitem__(item,value)
		for i in range(self.zone.start_id, self.zone.end_id+1):
			self.zone.segments[i].__dict__[item]=value

class TwoDParamsZone(dict):
	def __init__(self,terrain,start,end):
		self.start_id=start
		self.end_id=end
		self.segments=terrain.segments
		self["color"]=[0,0,0]
		self["params"]=TwoDParamsDict(self,terrain)

class GenericTwoDCheckpoint(GenericCheckpoint):
	valid_input_attrs=ParametersDescriptorsSet([
		["x",			"_x",			"x [m]",		float,	0,		1e10,	10],
		["angle",		"angle",		"Angle [deg]",	float,	0,		360,	90],
		["max_height",	"max_height",	"Height [m]",	float,	-1,		100,	-1]
	])
	def __init__(self, _x=None, angle=None, max_height=None):
		for p in self.valid_input_attrs.parameters:
			value = None
			if (p.inst_name in locals()):
				value = locals()[p.inst_name]
			if (value is not None):
				p.set_to_obj(self, value) #this will set the value from kwargs
			else:
				p.set_to_obj(self) #this will set the default.
		self.color = [255, 255, 255]
		self.init_data_done = False
	def init_data(self,simulation=None):
		"""
		Initialize data lists: :attr:`rocks`, :attr:`heights`, :attr:`vels`, :attr:`angVels`
		"""
		self.init_data_done = True
		super().init_data()
		if(simulation is None or simulation.terrain is None):
			self.base_point = Math.Vector2([self._x,0])
		else:
			self.base_point=Math.Vector2([self._x,simulation.terrain.get_z(self._x)])
		angle_rads = np.radians(self.angle)
		self.dir_vect = Math.Vector2([np.cos(angle_rads), np.sin(angle_rads)])
		self.line=Geoms.Line(point=self.base_point, angle=angle_rads)
		self.heights=[]
	def get_plotting_coords(self, high_value=1e20):
		if(self.max_height<0):
			(end_x, end_z) = self.base_point + self.dir_vect * high_value
		else:
			(end_x, end_z) = self.base_point + self.dir_vect * self.max_height
		return np.array([self.base_point,[end_x, end_z]])

class GenericTwoDTerrain(GenericTerrain):
	"""
	A 2D terrain made of segments.
	
	Args:
		file (string):
		
	Attributes:
		segments (list): the successive :class:`GenericSegment` forming the terrain
		rebound_models_available (list): A list of available bounce models numbers regarding the per-segment input parameters given, automatically filled.
		forest_available (bool): whether the forest is available in the terrain regarding the per-segment input parameters given, automatically set.
	"""
	
	valid_input_attrs=GenericSegment.valid_input_attrs # set in subclasses
	
	def __init__(self,file=None):
		super().__init__()
		self.segments=[]
		self.params_zones=[]
		self.forest_available=False
		if (file is not None):
			self.import_from_csv(file)
			self.check_segments_continuity()
			self.check_segments_parameters_consistency()
			self.index_segments()
			self.set_params_zones()
	
	def import_from_csv(self,file):
		"""
		Args:
			file (string): path to the terrain file. This file is a basic csv text file, which contains points (X,Z) and per-segment parameters. It is formed as follows:
			
				+-+-+-------------------+---+---+---------+------+---+-------------+--------------+-------------+
				|X|Z|bounce_model_number|R_t|R_n|roughness|v_half|phi|trees_density|trees_dhp_mean|trees_dhp_std|
				+-+-+-------------------+---+---+---------+------+---+-------------+--------------+-------------+

				The first line of the file MUST be the columns names, which are CASE-SENSITIVE but the sequence can be swapped. The data must be rectangular, meaning that the table must be fullfilled without "no-data" possibility. You can import a terrain with only X and Z columns, but in this case you will have to complete the segments parameters in your script before launching the simulation.
		
		"""
		_segments_type = self.get_parent_module().Segment
		### all these code lines are needed to clean the terrain.
		input_array=np.genfromtxt(file,names=True, dtype=float)
		if(input_array['Z'][0]-input_array['Z'][-1]<0): # mirror terrain through X if the terrain is ascendent
			input_array['X']=-input_array['X']
			input_array['X']-=input_array['X'].min()
		if(input_array['X'][-1]-input_array['X'][0]<0):	# reverse the values through X if they are inversed
			input_array=np.flip(input_array,axis=0)
		# add horizontal segments at the right and left
		#input_array=np.append(input_array,[input_array[-1]]) ; input_array[-1]["X"]+=0.1*(input_array[-1]["X"]-input_array[0]["X"])
		#input_array=np.insert(input_array,0,[input_array[0]]) ; input_array[0]["X"]-=0.1*(input_array[-1]["X"]-input_array[0]["X"])
		
		### BEGIN REMOVE CAVITIES
		# 1:sort indices by X position in a new list and delete indices that creates cavities
		cleaned_indices=[]
		sorted_indices=np.argsort(input_array['X'])
		unsorted_indices=list(range(len(sorted_indices)))
		counter=0
		while counter < len(sorted_indices):
			i=sorted_indices[counter]
			if(i==unsorted_indices[0]):		# no cavity
				cleaned_indices.append(i)
				unsorted_indices.pop(0)
			else:							# there is a cavity here. Compute V1 and V2 to know whether its a cavity towards left or right of the terrain
				V1=Math.Vector2([input_array[i]['X'],input_array[i]['Z']])-Math.Vector2([input_array[unsorted_indices[0]]['X'],input_array[unsorted_indices[0]]['Z']])
				V2=Math.Vector2([input_array[cleaned_indices[-1]]['X'],input_array[cleaned_indices[-1]]['Z']])-Math.Vector2([input_array[unsorted_indices[0]]['X'],input_array[unsorted_indices[0]]['Z']])
				if(V1.cross(V2)[0]<0):	# so the cavity is on the LEFT
					unsorted_indices.remove(i)
				else:						# so the cavity is on the RIGHT
					for j in range(counter,i):
						counter+=1
						unsorted_indices.remove(j)
					cleaned_indices.append(i)
					unsorted_indices.remove(i)
			counter+=1
		
		# 2: at each discontinuity (one per cavity), add a point that makes the terrain locally vertical (fill the cavity)
		new_cleaned_indices=cleaned_indices[:]
		for cleaned_indice in range(len(cleaned_indices)-1):
			i=cleaned_indices[cleaned_indice]	#the indice of the point before the discontinuity
			j=cleaned_indices[cleaned_indice+1]	#the indice of the point after the discontinuity
			if(j>i+1):	# so there is a discontinuity
				if(input_array[i]['Z']>input_array[j]['Z']): #LEFT side cavity
					line=Geoms.Line(S=_segments_type([input_array[j-1]['X'],input_array[j-1]['Z']],[input_array[j]['X'],input_array[j]['Z']]))
					x=input_array[i]['X']
					z=line.a*x+line.b
					new_cleaned_indices.insert(cleaned_indice+1+(len(new_cleaned_indices)-len(cleaned_indices)),j-1)
					input_array[j-1]["X"]=x
					input_array[j-1]["Z"]=z
				else:	#RIGHT side cavity
					line=Geoms.Line(S=_segments_type([input_array[i]['X'],input_array[i]['Z']],[input_array[i+1]['X'],input_array[i+1]['Z']]))
					x=input_array[j]['X']
					z=line.a*x+line.b
					new_cleaned_indices.insert(cleaned_indice+1+(len(new_cleaned_indices)-len(cleaned_indices)),i+1)
					input_array[i+1]["X"]=x
					input_array[i+1]["Z"]=z
		
		### BEGIN ADD SLOPE TO VERTICAL SEGMENTS
		for indice in range(len(new_cleaned_indices)):
			i=new_cleaned_indices[indice]
			xa=input_array[i]["X"] ; za=input_array[i]["Z"]
			for j in new_cleaned_indices[indice+1:-1]:
				xb=input_array[j]["X"] ; zb=input_array[j]["Z"]
				if(abs(zb-za)<1e-8):	#HORIZONTAL
					break
				neg_slope=(zb-za)<0.
				theta1=np.arctan(abs((xb-xa)/(zb-za)))
				if(neg_slope and theta1<np.radians(1.)):
					input_array[j]["X"]=input_array[i]["X"]+np.tan(np.radians(1.))*(input_array[i]["Z"]-input_array[j]["Z"])
				elif((not neg_slope) and theta1<np.radians(1.) ):
					input_array[j]["X"]=input_array[i]["X"]-np.tan(np.radians(1.))*(input_array[i]["Z"]-input_array[j]["Z"])
				else:
					break
					
		### FINALLY REPLACE THE INPUT_ARRAY
		input_array=input_array[new_cleaned_indices]
		
		### Create segments with X,Z and columns names
		for i in range(0,len(input_array)-1):
			# in all cases, import the terrain coordinates:
			if( abs(input_array['X'][i] - input_array['X'][i+1])<1e-3 and abs(input_array['Z'][i] - input_array['Z'][i+1])<1e-3 ): # consecutive points at the same place
				continue
			s=_segments_type([input_array['X'][i],input_array['Z'][i]],[input_array['X'][i+1],input_array['Z'][i+1]])
			for column_name in input_array.dtype.fields:
				param_descriptor=self.valid_input_attrs.get_param_by_input_name(column_name)
				if(param_descriptor):
					param_descriptor.set_to_obj(s,input_array[column_name][i])
			self.segments.append(s)
	
	def get_csv_string(self):
		s='X	Z'
		params_names=self.valid_input_attrs.get_instance_names()
		for p in params_names:
			s+="\t"+p
		s=s+"\n"
		for segt in self.segments:
			s+=str(segt.points[0][0])+"\t"+str(segt.points[0][1])+"\t"
			for p in params_names:
				s+=str(segt.__dict__[p])+"\t"
			s=s[:-1]+"\n"
		segt=self.segments[-1]
		s+=str(self.segments[-1].points[1][0])+"\t"+str(self.segments[-1].points[1][1])+"\t"
		for p in params_names:
			s+=str(segt.__dict__[p])+"\t"
		s=s[:-1]
		return s
	
	def check_segments_continuity(self):
		"""
		Checks the continuity of the terrain. This method checks that each segment starts at the previous segment end. Is the terrain is not valid, the program exits.
		"""
		valid=True
		for i in range(1,len(self.segments)-1):
			if(abs(self.segments[i].points[1,0]-self.segments[i+1].points[0,0])>1e-10):valid=False
			if(abs(self.segments[i].points[1,1]-self.segments[i+1].points[0,1])>1e-10):valid=False
		if(not valid):
			Debug.info("ERROR, the terrain is not valid")
			sys.exit(1)
	
	def check_segments_forest_parameters_consistency(self):
		s=self.segments[0] #all the segments has the same data, use the first one to list them below
		HAS_trees_density=s.trees_density is not None
		HAS_dhp=(s.trees_dhp_mean is not None) and (s.trees_dhp_std is not None)
		if(HAS_dhp and HAS_trees_density):
			self.forest_available=True

	def check_segments_parameters_consistency(self):
		"""
			Analyze the segments parameters and checks their consistency/availability. :attr:`forest_available` and :attr:`rebound_models_available` are here.
		"""
		self.check_segments_forest_parameters_consistency()
	
	def compare_params(self,id1,id2):
		s1=self.segments[id1]
		s2=self.segments[id2]
		for param_name in self.valid_input_attrs.get_instance_names():
			if(s1.__dict__[param_name]!=s2.__dict__[param_name]):
				#NOTE: in numpy (np.nan == np.nan) returns False, but two nan values must be considered as identical here.
				if (np.isnan(s1.__dict__[param_name]) and np.isnan(s2.__dict__[param_name])):
					continue
				return False
		return True
		
	def set_params_zones(self):
		if len(self.segments) < 1 :
			self.params_zones=[]
			return
		self.params_zones=[TwoDParamsZone(self,0,0)] #init with first segment = first zone
		for id1 in range(1,len(self.segments)):
			id2 = self.params_zones[-1].end_id
			if(self.compare_params(id1,id2)):	#so we are still on the same param zone, increase its size
				self.params_zones[-1].end_id=id1
			else:	#so we enter a new zone
				self.params_zones.append(TwoDParamsZone(self,id1,id1))
		i=0
		for pz in self.params_zones:
			pz["color"]=ColorPalettes.qualitative10[i]
			i+=1
	
	def point_is_a_zone_border(self,x):
		id1, id2 = self.get_segments_ids_around_point(x)
		if(id1==-1 or id2==-1): return True
		for pz in self.params_zones:
			if(id1>=pz.start_id and id1<=pz.end_id and id2>=pz.start_id and id2<=pz.end_id):
				return False
		return True

	def get_z(self,x):
		for s in self.segments:
			if(s.points[0,0]<=x and s.points[1][0]>=x):
				return s.get_z(x)
		#x is outside the terrain
		if x>=self.get_points()[-1,0] :
			return self.get_points()[-1,1]
		elif x<=self.get_points()[0,0]:
			return self.get_points()[0,1]
		else:
			Debug.error("Error in terrain.get_z, should never happen.")
	
	def get_segment_zone_ids(self,index):
		for pz in self.params_zones:
			if(index>=pz.start_id and index<=pz.end_id):
				return [pz.start_id,pz.end_id]
				
	def get_points(self):
		"""
		From the list of segments, returns an array of points representing the terrain.
		#FIXME: this method should be used once, but it seems to be used very often during simulation
		
		Returns:
			:class:`numpy.ndarray` [[x0, z0], [x1, z1], ...]
		"""
		output=np.asarray([seg.points[0,:] for seg in self.segments],dtype=float)
		output=np.append(output,[self.segments[-1].points[-1,:]],axis=0)
		return output
	
	def index_segments(self):
		"""
		Index all segments of the terrain, :math:`i=0..N`, applying :class:`GenericSegment` . :attr:`index` :math:`=i`
		As the index are continuously distributed along the terrain, it allows to easily access the next or the previous segment from a given segment.
		"""
		for i in range(0,len(self.segments)):
			self.segments[i].index=i
	
	def get_angle_between(self,id1,id2):
		if(id1>id2):
			id1,id2=id2,id1
		seg1=self.segments[id1]
		seg2=self.segments[id2]
		ret = math.atan2(seg1.points[0][1]-seg1.points[1][1],seg1.points[0][0]-seg1.points[1][0])- math.atan2(seg2.points[1][1]-seg2.points[0][1],seg2.points[1][0]-seg2.points[0][0])
		if(ret<0):
			ret+=np.pi*2
		return ret
	
	def get_z_range(self):
		pts=self.get_points()[:,1]
		return [pts.min(), pts.max()]

	def get_x_range(self):
		pts=self.get_points()[:,0]
		return [pts.min(), pts.max()]
	
	def get_segments_ids_around_point(self,x):
		nearest=np.inf
		for s in self.segments:
			if abs(s.points[0][0]-x)<nearest:
				best_segts = [s.index-1, s.index]
				nearest=abs(s.points[0][0]-x)
		if abs(self.segments[-1].points[1][0]-x)<nearest:
			best_segts = [ len(self.segments)-1, -1]
		return best_segts

	def remove_point(self,x):
		id1, id2 = self.get_segments_ids_around_point(x)
		if(id2==-1): #remove the last point, so remove segment n°id1
			self.remove_segment(id1)
			return
		if id2==len(self.segments)-1 : #remove the penultimate point, so remove the last segment but connect end of id1 to end of id2 before.
			self.segments[id1].points[1][:]=self.segments[id2].points[1][:]
		#general case: remove the segment after the point at x
		self.remove_segment(id2)
	
	def add_point_after(self,x):
		id1, id2 = self.get_segments_ids_around_point(x)
		if(id2!=-1): #if there is a segment after the point
			self.split_segment(id2)
	
	def move_point(self,x,newx,newy):
		id1, id2 = self.get_segments_ids_around_point(x)
		if(id1==-1):
			self.move_segment_point(0,"start",newx,newy)
		elif(id2==-1):
			self.move_segment_point(len(self.segments)-1,"end",newx,newy)
		else:
			self.move_segment_point(id1,"end",newx,newy)
	
	def new_zone_at(self,x):
		id1, id2 = self.get_segments_ids_around_point(x)
		if not self.point_is_a_zone_border(x) :
			zone_start, zone_end = self.get_segment_zone_ids(id2)
			for index in range(id2,zone_end+1):
				for p in self.valid_input_attrs.parameters:
					p.set_to_obj(self.segments[index]) #no value given to set_to_obj => default value set.
		self.set_params_zones()

	def remove_segment(self,id):
		if(id!=0 and id!=len(self.segments)-1): #if the segment is not at an extremity, update the end point of the previous segment.
			self.segments[id-1].points[1][:]=self.segments[id].points[1][:]
			self.segments[id-1].set_geometrical_quantities()
		self.segments.pop(id)
		self.index_segments()
		self.set_params_zones()
		self.check_segments_continuity()
		self.check_segments_parameters_consistency()
	
	def split_segment(self,id):
		middle_point = (self.segments[id].points[0] + self.segments[id].points[1])/2
		new_segt=copy.deepcopy(self.segments[id])
		self.segments[id].points[1]=middle_point[:]
		self.segments[id].set_geometrical_quantities()
		new_segt.points[0]=middle_point[:]
		new_segt.set_geometrical_quantities()
		self.segments.insert(id+1,new_segt)
		self.index_segments()
		self.set_params_zones()
		self.check_segments_continuity()
		self.check_segments_parameters_consistency()
	
	def move_segment_point(self,index,which_end,x,y):
		eps=1e-4
		if(which_end=="start"):
			x=min(x,self.segments[index].points[1][0]-eps)
			if(index!=0):
				x=max(x,self.segments[index-1].points[0][0]+eps)
			self.segments[index].points[0][0]=x
			self.segments[index].points[0][1]=y
			self.segments[index].set_geometrical_quantities()
			if(index!=0):
				self.segments[index-1].points[1][0]=x
				self.segments[index-1].points[1][1]=y
				self.segments[index-1].set_geometrical_quantities()
		elif(which_end=="end"):
			x=max(x,self.segments[index].points[0][0]+eps)
			if(index!=len(self.segments)-1):
				x=min(x,self.segments[index+1].points[1][0]-eps)
			self.segments[index].points[1][0]=x
			self.segments[index].points[1][1]=y
			self.segments[index].set_geometrical_quantities()
			if(index!=len(self.segments)-1):
				self.segments[index+1].points[0][0]=x
				self.segments[index+1].points[0][1]=y
				self.segments[index+1].set_geometrical_quantities()
		self.index_segments()
		self.set_params_zones()
		self.check_segments_continuity()
		self.check_segments_parameters_consistency()
		
	def get_zone_at_x(self,x):
		for zone in self.params_zones:
			if self.segments[zone.start_id].points[0,0] < x and self.segments[zone.end_id].points[1,0] >= x:
				return zone
		return False