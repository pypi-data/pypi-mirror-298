from platrock.Common.Simulations import GenericSimulation
from platrock.Common.Utils import ParametersDescriptorsSet
from platrock.Common import Math, Outputs, Debug
from platrock.TwoD import Geoms
import numpy as np
import zipfile, os

import platrock

class GenericTwoDSimulation(GenericSimulation):
	"""
	Args:
		terrain (:class:`TwoD.Objects.Terrain`): the terrain of the simulation 
		gravity (float): the --- positive --- gravity acceleration value
		rocks (list [:class:`TwoD.Objects.Rock`]): list of rocks, automatically filled
		checkpoints (list [:class:`TwoD.Objects.Checkpoint`, ...]): all the checkpoints. Checkpoints data are post-computed with :meth:`update_checkpoints` from all contacts of all rocks.
		name (String): the name of the simulation, mandatory for the WebGUI
		rocks_start_params (dict): a dictionnary of the rocks start parameters (see Examples/2D.py for more details)
		status (String): available status: ["init"|"running"|"pause"|"finished"|"error"]
		
		nb_rocks (int): number of rocks to launch
		rocks_volume (float): volume of the rocks
		rocks_density (float): density of the rocks
		rocks_x (float): initial x corrdinate of the rocks
		rocks_z (float): initial height of the rocks
		rocks_vx (float): initial horizontal velocity of the rocks
		rocks_vz (float): initial vertical velocity of the rocks
		rocks_angVel (float): initial angular velocity of the rocks
		
		override_rebound_params (bool): if True, the rebound parameters will be overriden by :attr:`override_roughness`, :attr:`override_R_n`, :attr:`override_R_t`, :attr:`override_phi`, :attr:`override_v_half` and :attr:`override_bounce_model_number`
		override_forest_params (bool): if True, the forest parameters will be overriden by :attr:`override_enable_forest` :attr:`override_trees_density` and :attr:`override_trees_dhp_mean` and :attr:`override_trees_dhp_std`
		override_enable_forest (bool)
		override_bounce_model_number=None
		override_roughness=None
		override_R_n=None
		override_R_t=None
		override_phi=None
		override_v_half=None
		override_trees_density=None
		override_trees_dhp_mean=None
		override_trees_dhp_std=None
	"""

	valid_rocks_start_params=ParametersDescriptorsSet([
		["nb_rocks",			"nb_rocks",			"Rocks count",						int,		1,		1000000,	100		],
		["rocks_min_vol",		"rocks_min_vol",	"Min rocks volume (m<sup>3</sup>)",	float,		1e-06,	100.,	1		],
		["rocks_max_vol",		"rocks_max_vol",	"Max rocks volume (m<sup>3</sup>)",	float,		1e-06,	100.,	2		],
		["rocks_vx",			"rocks_vx",			"Horizontal velocity (m/s)",		float,		-100,	100,		1		],
		["rocks_vz",			"rocks_vz",			"Vertical velocity (m/s)",			float,		-100,	100,		0		],
		["rocks_angVel",		"rocks_angVel",		"Angular velocity (rad/s)",			float,		-6.3,	6.3,	0		],
		["rocks_min_x",			"rocks_min_x",		"Min horizontal position (m)",		float,		0 ,		np.inf,	1		],
		["rocks_max_x",			"rocks_max_x",		"Max horizontal position (m)",		float,		0 ,		np.inf,	2		],
		["rocks_min_z",			"rocks_min_z",		"Min falling height (m)",			float,		0.1,	50,		5		],
		["rocks_max_z",			"rocks_max_z",		"Max falling height (m)",			float,		0.1,	50,		8		],
		["rocks_density",		"rocks_density",	"Density (kg/m<sup>3</sup>)",		float,		500,	5000,	2650	]
	])

	valid_retro_compatibility_params=ParametersDescriptorsSet([
		["rocks_volume",	"rocks_volume",	"Rocks volume (m<sup>3</sup>)",	float,		0.1,	100.,	1		],
		["rocks_x",			"rocks_x",		"Horizontal position (m)",		float,		0 ,		np.inf,	1		],
		["rocks_z",			"rocks_z",		"Falling height (m)",			float,		0.1,	50,		5		],
	])

	# Useful in generic classes implementation :
	NB_SPACE_DIMS = 2
	SPACE_VECTOR_CLASS = Math.Vector2
	
	def __init__(self, checkpoints_x=[], checkpoints_angles=[], checkpoints_max_heights=[], rocks_start_params={}, **kwargs):
		#FIXME : DOC
		"""
		Constructor
		
		Args:
			checkpoints_x (list [x0, x1, ...]): all the checkpoints x postions. Checkpoints data are post-computed with :meth:`update_checkpoints` from all contacts of all rocks.
		"""
		super().__init__(**kwargs)
		for p in self.get_terrain_cls().valid_input_attrs.parameters:
				p.set_to_obj(self,None,"override_")

		assert ( len(checkpoints_angles)==len(checkpoints_x) or len(checkpoints_angles)==0)
		assert ( len(checkpoints_max_heights)==len(checkpoints_x) or len(checkpoints_max_heights)==0)
		self.checkpoints = []
		for i,x in enumerate(checkpoints_x):
			kw_dict = {}
			if (len(checkpoints_angles)!=0): kw_dict['angle'] = checkpoints_angles[i]
			if (len(checkpoints_max_heights)!=0): kw_dict['max_height'] = checkpoints_max_heights[i]
			self.checkpoints.append( self.get_parent_module().Objects.Checkpoint(x, **kw_dict) )
		
		# SET THE ROCKS DEFAULT PARAMS :
		for p in self.valid_rocks_start_params.parameters:
			p.set_to_obj(self)

		#OVERRIDE THE DEFAULT PARAMS, IF AVAILABLE IN rocks_start_params dict.
		for k in rocks_start_params.keys():
			param_descriptor=self.valid_rocks_start_params.get_param_by_input_name(k)
			if(param_descriptor):
				param_descriptor.set_to_obj(self,rocks_start_params[k])
		#IMPORT RETRO-COMPATIBILITY PARAMETERS IF GIVEN
		for k in rocks_start_params.keys():
			param_descriptor=self.valid_retro_compatibility_params.get_param_by_input_name(k)
			if(param_descriptor):
				param_descriptor.set_to_obj(self,rocks_start_params[k])
		self.apply_retro_compatibility()
		self.__init_arrays__()
	
	def apply_retro_compatibility(self):
		if hasattr(self,"rocks_volume"):
			self.rocks_min_vol=self.rocks_volume
			self.rocks_max_vol=self.rocks_volume
		if hasattr(self,"rocks_x"):
			self.rocks_min_x=self.rocks_x
			self.rocks_max_x=self.rocks_x
		if hasattr(self,"rocks_z"):
			self.rocks_min_z=self.rocks_z
			self.rocks_max_z=self.rocks_z
	
	def __init_arrays__(self):
		#Handle generated arrays based on params. This method is run at simulation instanciation and during before_run_tasks in case of web_ui usage: this allows script users to manually change it.
		self.rocks_volumes=self.random_generator.rand(self.nb_rocks)*(self.rocks_max_vol - self.rocks_min_vol)+self.rocks_min_vol
		self.rocks_start_x=self.random_generator.rand(self.nb_rocks)*(self.rocks_max_x - self.rocks_min_x)+self.rocks_min_x
		self.rocks_start_z=self.random_generator.rand(self.nb_rocks)*(self.rocks_max_z - self.rocks_min_z)+self.rocks_min_z
		
	def save_to_file(self):
		"""
		Store (pickle to json) the simulation into a file whose path and name is the return result of :meth:`get_dir`. Note that the file will exclude all data that arises from calculations, this method is meant to save the simulation setup only.
		"""
		#store to local variables all data that shouldn't be saved to the file, then clear the corresponding simulation attributes :
		output=self.output
		self.output=None
		checkpoints=self.checkpoints[:]
		self.checkpoints=[self.get_parent_module().Objects.Checkpoint(c._x, c.angle, c.max_height) for c in checkpoints] #NOTE: keep the checkpoints position, drop the data
		if(self.terrain): #don't save the params zones as it's not necessary and jsonpickle don't deal with this weird types
			params_zones=self.terrain.params_zones
			self.terrain.params_zones=[]
		if hasattr(self,'mechanicsHdf5Runner'):
				mechanicsHdf5Runner = self.mechanicsHdf5Runner
				self.mechanicsHdf5Runner=None
		if hasattr(self,"current_DS"):
			current_DS = self.current_DS
			self.current_DS = None
		if hasattr(self,"siconos_run_options"):
			siconos_run_options = self.siconos_run_options
			self.siconos_run_options = None
		if hasattr(self,"last_rock_zone"):
			self.last_rock_zone=None
		super().save_to_file()	#actual file write is here. Don't use super as save_to_file is imported in TwoDShape.
		#restore the not-saved data:
		self.output=output
		self.checkpoints=checkpoints
		if(self.terrain):
			self.terrain.params_zones=params_zones
		if hasattr(self,'mechanicsHdf5Runner'):
			self.mechanicsHdf5Runner=mechanicsHdf5Runner
		if hasattr(self,"current_DS"):
			self.current_DS = current_DS
		if hasattr(self,"siconos_run_options"):
			self.siconos_run_options = siconos_run_options
		Debug.info("... DONE")
	
	def update_checkpoints(self):
		"""
		Update all the simulation :class:`TwoD.Objects.Checkpoint` according to all contacts of all rocks. This is a post-treatement feature, it is supposed to be triggered after the simulation is terminated.
		"""
		#FIXME: there seems to be a bug when checkpoint position == contact pos, or initial rock pos.
		for chkP in self.checkpoints:
			chkP.init_data(self)
		
		for ri in range(self.nb_rocks):
			contacts_types=self.output.get_contacts_types(ri)
			if (contacts_types==Outputs.MOTION).any():
				self.update_checkpoints_motion_contacts(ri)
			else:
				self.update_checkpoints_soil_roll_contacts(ri, contacts_types)

		for chkP in self.checkpoints:
			chkP.crossings_ratio=len(chkP.heights)/self.nb_rocks
		self.output.checkpoints=self.checkpoints
	
	def update_checkpoints_soil_roll_contacts(self, ri, contacts_types): # this will work for material-point simulations, with contacts of type {START, SOIL, ROLL, TREE}
		checkpoints = self.checkpoints.copy() # shallow copy !
		contacts_pos=self.output.get_contacts_pos(ri)
		contacts_vels=self.output.get_contacts_vels(ri)
		contacts_angVels=self.output.get_contacts_angVels(ri)
		for ci in range(len(contacts_types)-1):
			contact_type = contacts_types[ci]
			contact_pos = contacts_pos[ci]
			contact_vel = contacts_vels[ci]
			contact_angVel = contacts_angVels[ci]
			next_contact_pos = contacts_pos[ci+1]
			chkP_idx = 0
			while(chkP_idx<len(checkpoints)):
				chkP = checkpoints[chkP_idx]
			# for chkP in checkpoints:
				if (contact_type == Outputs.ROLL):
					if (contact_pos[0]<chkP.base_point[0]<next_contact_pos[0] or contact_pos[0]>chkP.base_point[0]>next_contact_pos[0]):
						checkpoints.pop(chkP_idx) # in this case, no need to increment chkP_idx
						chkP.rocks_ids.append(ri)
						chkP.heights.append(0.0)
						v0_square=Math.Vector2(contacts_vels[ci]).norm()**2
						vf_square=Math.Vector2(contacts_vels[ci+1]).norm()**2
						d_tot=Math.Vector2(contact_pos-next_contact_pos).norm()
						dist_ratio = (chkP.base_point[0]-contact_pos[0])/(next_contact_pos[0]-contact_pos[0])
						d=d_tot*dist_ratio
						vel=np.sqrt( (vf_square-v0_square)/d_tot * d + v0_square )
						chkP.vels.append(vel*Math.Vector2(next_contact_pos-contact_pos).normalized())
						chkP.angVels.append(vel/((3*self.output.volumes[ri]/4/np.pi)**(1/3)))
					else:
						chkP_idx += 1
				else:# (contact_type == Outputs.SOIL or contact_type == Outputs.TREE or contact_type == Outputs.START):
					parabola=Geoms.Parabola(pos=Math.Vector2(contact_pos),vel=Math.Vector2(contact_vel),g=self.gravity)
					intersections = Geoms.get_line_parabola_intersections(chkP.line, parabola)
					valid_intersections = []
					# 1- remove intersections that are not inside the rock fly range.
					for intersection in intersections:
						if (contact_pos[0] < next_contact_pos[0] and (intersection[0]>=contact_pos[0] and intersection[0]<=next_contact_pos[0])):
							valid_intersections.append(intersection)
						elif (next_contact_pos[0] < contact_pos[0] and (intersection[0]>=next_contact_pos[0] and intersection[0]<=contact_pos[0])):
							valid_intersections.append(intersection)
					intersections = valid_intersections.copy()
					valid_intersections = []
					# 2- remove intersections that are not in the "good" half line of the checkpoint. For finite length checkpoints, remove intersections that are too high.
					for intersection in intersections:
						intersection = Math.Vector2(intersection)
						if (
							chkP.dir_vect.dot(intersection-chkP.base_point)>0 and  #good half line
							( chkP.max_height<0 or (intersection-chkP.base_point).norm() < chkP.max_height) #finite length, too high intersection
						):
							valid_intersections.append(intersection)
					# 3- now check the number of valid_intersections to decide what to do
					if (len(valid_intersections)==0): #checkpoint not crossed
						chkP_idx+=1
						continue #to next checkpoint
					elif (len(valid_intersections)==1):
						valid_intersection = valid_intersections[0]
					elif (len(valid_intersections)==2):
						#we still have two intersections, just keep the first one crossed
						if (contact_pos[0] < next_contact_pos[0]): #rock goes towards +X
							if (valid_intersections[0][0]<valid_intersections[1][0]):
								valid_intersection = valid_intersections[0]
							else:
								valid_intersection = valid_intersections[1]
						else: #rock goes towards -X
							if (valid_intersections[0][0]<valid_intersections[1][0]):
								valid_intersection = valid_intersections[1]
							else:
								valid_intersection = valid_intersections[0]
					checkpoints.pop(chkP_idx) # in this case, no need to increment chkP_idx
					chkP.rocks_ids.append(ri)
					chkP.heights.append( (valid_intersection-chkP.base_point).norm() )
					chkP.vels.append(contact_vel.copy()) #make a copy as we modify the value below, and don't want to modify the s.output.contacts arrays
					chkP.vels[-1][1]=-self.gravity*(valid_intersection[0]-contact_pos[0])/contact_vel[0] + contact_vel[1]
					chkP.angVels.append(contact_angVel)
	
	def update_checkpoints_motion_contacts(self, ri): # this will work for shape simulations, with contacts of type {START, MOTION, TREE}
		for chkP in self.checkpoints:
			contacts_pos=np.copy(self.output.get_contacts_pos(ri))
			contacts_ids = np.arange(len(contacts_pos),dtype=int)
			contacts_pos -= chkP.base_point # C.S. translation to set origin to chkP base_point
			cross_prods_signs = np.sign(np.cross(contacts_pos, chkP.dir_vect)) # use the cross product and keep its sign to detect whether rock_pos is above or below chkP_line
			chkp_line_crossed_ids = np.where(cross_prods_signs[:-1] != cross_prods_signs[1:])[0] # this gives the rock_pos ids just before the rock crosses the chkP_line
			if(len(chkp_line_crossed_ids)>0):
				contacts_ids = contacts_ids[chkp_line_crossed_ids]
				pos_before_crosses = contacts_pos[chkp_line_crossed_ids] #this gives the rock_pos just before the rock crosses the chkP_line.
				pos_after_crosses = contacts_pos[chkp_line_crossed_ids+1] #this gives the rock_pos just after the rock crosses the chkP_line.
				# at this stage we calculate the intersection between :
				# 1- the rock branch vector from position pos_before_crosses and its position right after, with the checkpoint intersection parametrized by "k", and
				# 2- the checkpoint segment or half-line, with the rock intersection parametrized by "m", normalized by the checkpoint dir unity vector.
				b_vs = pos_after_crosses - pos_before_crosses #branch vectors crossing the checkpoint line
				denoms = chkP.dir_vect[1]*b_vs[:,0] - chkP.dir_vect[0]*b_vs[:,1] #finding "k" as well as "m" requires this denominator
				valid_denoms_ids = np.where(abs(denoms)>chkP.line.EPS)[0] #filter out trajectories that are parallel to the checkpoint.
				b_vs=b_vs[valid_denoms_ids]; denoms=denoms[valid_denoms_ids]; pos_before_crosses=pos_before_crosses[valid_denoms_ids]; contacts_ids=contacts_ids[valid_denoms_ids]
				k = (pos_before_crosses[:,1]*chkP.dir_vect[0] - pos_before_crosses[:,0]*chkP.dir_vect[1]) / denoms
				m = (pos_before_crosses[:,1]*b_vs[:,0] - pos_before_crosses[:,0]*b_vs[:,1]) / denoms
				assert (0<=k).all() # we already checked that with the cross product above
				assert (1>=k).all() # we already checked that with the cross product above
				if (chkP.max_height<0):
					valid_ids = np.where(m>=0)[0]
				else:
					valid_ids = np.where((m>=0) & (m<=chkP.max_height))[0] #we can compare m to max_height because m is computed from the checkpoint unity vector
				if (len(valid_ids)):
					valid_id = valid_ids[0] #only keep the first rock-checkpoint crossing
					valid_m = m[valid_id]
					valid_k = k[valid_id]
					valid_contact_id = contacts_ids[valid_id]
					intersection = valid_m * chkP.dir_vect + chkP.base_point
					chkP.rocks_ids.append(ri)
					chkP.heights.append(valid_m)
					vel=self.output.get_contacts_vels(ri)[valid_contact_id]
					if (len(self.output.get_contacts_vels(ri))>valid_contact_id+1):
						vel_after=self.output.get_contacts_vels(ri)[valid_contact_id+1]
					else:
						vel_after=vel #likely not to happen
					angVel=self.output.get_contacts_angVels(ri)[valid_contact_id]
					chkP.vels.append((1-valid_k)*vel+valid_k*vel_after) #linear velocity interpolation between two known values
					chkP.angVels.append(angVel)
	
	def get_stops_cdf(self,nbins=200):
		xmax=np.zeros(self.output._rocks_counter)
		if (self.output is not None) and self.output._rocks_counter>0 :
			for r_id in range(0,self.output._rocks_counter):
				xmax[r_id] = self.output.get_contacts_pos(r_id)[:,0].max()
		xmax.sort()
		rocks_out_of_bounds_count=np.sum(xmax>self.terrain.get_points()[-1,0]) 
		hist,bin_edges=np.histogram(xmax,np.linspace(self.terrain.segments[0].points[0][0],self.terrain.segments[-1].points[1][0],nbins))
		hist=np.cumsum(hist)
		hist=np.append(hist,hist[-1])
		hist=hist/(hist.max()+rocks_out_of_bounds_count)
		out=np.zeros([2,len(hist)])
		out[0,:]=bin_edges
		out[1,:]=hist
		return out
		
	
	def results_to_zipfile(self,filename=None):
		"""
		Create a zip file into the folder returned by :meth:`get_dir` named results.zip containing two text files. "stops.csv" contains info about rocks end position, and "checkpoints.csv" contains the checkpoints infos.
		"""
		self.output.write_to_h5(self.get_dir()+'full_output.hdf5')
		if(filename is None):
			filename=self.get_dir()+"results.zip"
		zf = zipfile.ZipFile(filename, "w")
		zf.write(self.get_dir()+'full_output.hdf5', 'full_output.hdf5')
		output_str="volume;x_stop\n"
		for i in range(self.nb_rocks):
			output_str+=str(self.output.volumes[i])+";"+str(self.output.get_contacts_pos(i)[-1,0])+"\n"
		zf.writestr("stops.csv",output_str)
		
		output_str="rock_id;x_checkpoint;y_checkpoint;height_checkpoint;angle_checkpoint;vx;vz;volume;height;angVel;Ec_t;Ec_r\n"
		for chckpt in self.checkpoints:
			for i in range(len(chckpt.heights)):
				rock_id=chckpt.rocks_ids[i]
				mass=self.output.volumes[rock_id]*self.output.densities[rock_id]
				output_str+=str(rock_id)+";"
				output_str+=str(chckpt.base_point[0])+";"
				output_str+=str(chckpt.base_point[1])+";"
				output_str+=str(chckpt.max_height)+";"
				output_str+=str(chckpt.angle)+";"
				output_str+=str(chckpt.vels[i][0])+";"
				output_str+=str(chckpt.vels[i][1])+";"
				output_str+=str(self.output.volumes[rock_id])+";"
				output_str+=str(chckpt.heights[i])+";"
				output_str+=str(chckpt.angVels[i])+";"
				output_str+=str(0.5*mass*Math.Vector2(chckpt.vels[i]).norm()**2)+";"
				output_str+=str(0.5*self.output.inertias[rock_id]*chckpt.angVels[i]**2)+"\n"
		zf.writestr("checkpoints.csv",output_str)
		
		if(os.path.isfile(self.get_dir()+"terrain_overview.pdf")):
			zf.write(self.get_dir()+"terrain_overview.pdf",arcname="trajectories_overview.pdf")
		zf.close()
	
	def before_run_tasks(self):
		super().before_run_tasks()
		if platrock.web_ui:
			self.__init_arrays__()
	
	def before_rock_launch_tasks(self):
		self.add_rock()
		self.setup_rock_kinematics()
		self.current_rock.update_current_segment(self.terrain)
		self.current_rock.pos[1]+=self.current_rock.current_segment.get_z(self.current_rock.pos[0])
		super().before_rock_launch_tasks()
	
	def after_rock_propagation_tasks(self,*args,**kwargs):
		super().after_rock_propagation_tasks(*args,**kwargs)
		if(self.current_rock.out_of_bounds):
			if (not platrock.SICONOS_FOUND) or (type(self)!=platrock.TwoDShape.Simulations.Simulation):
				#Fly into the void...
				parab=Geoms.Parabola(self.current_rock,g=self.gravity)
				terrain_Dx=self.terrain.get_points()[-1][0] - self.terrain.get_points()[0][0]
				if(self.current_rock.vel[0]>0):
					arrival_x=self.terrain.get_points()[-1][0]+0.05*terrain_Dx
				else:
					arrival_x=self.terrain.get_points()[0][0]-0.05*terrain_Dx
				self.current_rock.fly(Math.Vector2([arrival_x,parab.get_value_at(arrival_x)]),self,self.current_rock.current_segment)
			self.output.add_contact(self.current_rock,Math.Vector2([0.,0.]),Outputs.OUT)
		else:
			#Mark the stop position
			self.output.add_contact(self.current_rock,Math.Vector2([0.,0.]),Outputs.STOP)
	
	def after_successful_run_tasks(self,*args,**kwargs):
		super().after_successful_run_tasks(*args,**kwargs)
		self.update_checkpoints()
		if platrock.web_ui:
			import platrock.GUI.Plot2D as Plot2D
			with open(self.get_dir()+'terrain_overview_plotly.html','w') as f:
				if platrock.SICONOS_FOUND and isinstance(self,platrock.TwoDShape.Simulations.Simulation):
					f.write(Plot2D.get_plotly_raw_html(self,50))
				else:
					f.write(Plot2D.get_plotly_raw_html(self,100))
			self.results_to_zipfile()
