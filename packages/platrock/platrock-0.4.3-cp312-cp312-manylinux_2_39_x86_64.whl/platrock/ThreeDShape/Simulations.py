from platrock.Common.ThreeDSimulations import GenericThreeDSimulation
from platrock.Common.ShapeSimulations import GenericShapeSimulation
from platrock.Common.TimeSteppedSimulations import GenericTimeSteppedSimulation
from platrock.Common.Utils import ParametersDescriptorsSet, Report
from platrock.Common.ThreeDObjects import Point
from platrock.Common import Math, Outputs, Debug
from . import Objects
import quaternion, shapely, time
import numpy as np

from siconos.mechanics.collision.tools import Contactor
import siconos.numerics as sn
from siconos.mechanics.collision.bullet import cast_Contact5DR

class Simulation(GenericThreeDSimulation, GenericShapeSimulation, GenericTimeSteppedSimulation):
	webui_typename="PlatRock 3D-Shape"
	valid_input_rocks_attrs=GenericThreeDSimulation.valid_input_rocks_geojson_attrs + ParametersDescriptorsSet([
		["random_rocks_ori",	"random_rocks_ori",		"Random orientation",				bool,		True],
		["StringChoice", ["rocks_shape", "shape"],	"rocks_shape",	"Rocks shape",	'Parallelepiped', [sc.__name__ for sc in Objects.Rock.__subclasses__()]]
	])
	valid_input_rocks_geojson_attrs = valid_input_rocks_attrs
	#NOTE: below concatenate all the parameters from all 3DShape available shapes. Note that the ParametersDescriptorsSet class implements a duplicate avoidance mechanism.
	for shape in Objects.Rock.__subclasses__():
		valid_input_rocks_geojson_attrs+=shape.valid_shape_params
	#NOTE:
	# - valid_input_rocks_attrs are the rocks params that are common to all rocks shape types
	# - valid_input_rocks_geojson_attrs are all the rocks params possible, combining valid_input_rocks_attrs and all rock-shapes-specific parameters.
	
	def __init__(self, dt = 0.001, *args, **kwargs):
		GenericTimeSteppedSimulation.__init__(self, dt = dt)
		GenericThreeDSimulation.__init__(self, *args, **kwargs)
		GenericShapeSimulation.__init__(self)
		
	def setup_siconos(self):
		return GenericShapeSimulation.setup_siconos(self, sn.SICONOS_ROLLING_FRICTION_3D_NSGS)
	
	def add_terrain(self):
		heightmap_size_x=self.terrain.Z_raster.X[-1]
		heightmap_size_y=self.terrain.Z_raster.Y[-1]
		self.mechanicsHdf5Runner.add_height_map(
			'Terrain',
			self.terrain.Z_raster.data["Z"],
			(heightmap_size_x, heightmap_size_y),
			outsideMargin=self.outside_margin,
			insideMargin=self.inside_margin,
			# avoid_internal_edge_contact=True
		)
		offsets=[heightmap_size_x/2,heightmap_size_y/2,-self.outside_margin]	#because SiconosHeightmap is a rectangle heightmap centered at zero.
		self.mechanicsHdf5Runner.add_object(
			'terrain',
			[
				Contactor(
					'Terrain',
					collision_group=1
				)
			],
            translation=offsets
		)

		#TREES :
		lowest_terrain_point_z=self.terrain.points_as_array[:,2].min()
		highest_terrain_point_z=self.terrain.points_as_array[:,2].max()+50.
		cylinders_height=highest_terrain_point_z-lowest_terrain_point_z
		for i,t in enumerate(self.terrain.trees):
			self.mechanicsHdf5Runner.add_primitive_shape(
				'Tree'+str(i), #name
				'Cylinder', #shape type name
				(t.dhp/2/100, cylinders_height), #parameters : (radius, length)
				insideMargin=self.inside_margin,
				outsideMargin=self.outside_margin
			)
			q=quaternion.from_rotation_vector([np.pi/2,0,0])
			t._siconos_collision_group = 1
			t._siconos_translation = [t.pos[0],t.pos[1],lowest_terrain_point_z+cylinders_height/2.]
			t._siconos_orientation = [q.w,q.x,q.y,q.z]
			self.mechanicsHdf5Runner.add_object(
				'tree'+str(i),
				[
					Contactor(
						'Tree'+str(i),
						collision_group=t._siconos_collision_group
					)
				],
				translation = t._siconos_translation,
				orientation = t._siconos_orientation
			)
		
		#LAW :
		self.mechanicsHdf5Runner.add_Newton_impact_rolling_friction_nsl(
			'lawTerrain',
			e=0,
			mu=0.2,
			mu_r=0,
			collision_group1=1,
			collision_group2=0
		)
	
	def add_rock(self):
		params=self.rocks_start_params[self.current_start_params_id]['params']

		#NOTE: Actions at each start zone change:
		if self.current_start_params_rock_id==1: #we just changed the start params set
			rock_cls = Objects.Rock.get_subclass_from_name(params['rocks_shape'])
			if rock_cls == False:
				Debug.error('There is no ThreeDShape rock of type "',params['rocks_shape'],'", falling back to "Parallelepiped".')
				rock_cls = Objects.Parallelepiped
			#NOTE: in the next line, create a dict with
			#	- keys = the rock params needed by the rock shape
			#	- values = the rocks params values found in params (from geojson)
			rock_kwargs = {p.inst_name:params[p.inst_name] for p in rock_cls.valid_shape_params.parameters}
			self.current_rock=rock_cls(
				**rock_kwargs
			)
		else:
		# NOTE: check whether we should change the rock shape.
			if hasattr(self.current_rock, 'nb_diff_shapes') and params['nb_diff_shapes']>1 and self.current_start_params_rock_id>0 :
				# The following line gives an array of rocks number for which we should generate a new shape.
				shapes_changes_rocks_nb = np.where((np.arange(0,params['number'])%(params['number']/params['nb_diff_shapes'])).astype(int) == 0)[0]
				if self.current_start_params_rock_id in shapes_changes_rocks_nb:
					# Actually change the rock shape
					self.current_rock.generate()
					Debug.info('Generate new rock at rock nb ',self.current_start_params_rock_id,'. ','New vertices: ',self.current_rock.vertices)


		self.current_rock.density=params["density"]
		self.current_rock.set_volume(params["rocks_volumes"][self.current_start_params_rock_id-1]) #NOTE: current_start_params_rock_id starts at 1
		
		# for compatibility with 3D view :
		if self.GUI_enabled:
			self.current_rock.generate_TO_points_faces()
			self.current_rock.VTK_actor = None #this will trigger a new VTK actor to be drawn

	def setup_rock_kinematics(self, x=None, y=None):
		# add the rock
		params=self.rocks_start_params[self.current_start_params_id]['params']
		# Pick a start point x y
		start_point = Point(*self.pick_rock_start_xy(), np.nan)
		
		#FIXME: take the shape of the rock into account.
		#find the face below the rock then set the rock altitude:
			#1- use the faces bounding boxes in the (x,y) plane to get a rough list
		mins_check_outside = (start_point.pos[0:2]<self.terrain.faces_xyz_bb[:,0:3:2]).any(axis=1)
		maxs_check_outside = (start_point.pos[0:2]>self.terrain.faces_xyz_bb[:,1:5:2]).any(axis=1)
		inside_mask = np.logical_not(np.logical_or(mins_check_outside, maxs_check_outside))
			#2- loop on the faces list to get the face right below the rock
		for f in self.terrain.faces[inside_mask]:
			#find the corresponding face:
			if(f.is_point_inside_2D(start_point)):	#find the Z position of the rock right above the corresponding face
				start_point.pos[2] = -(f.normal[0]*(start_point.pos[0]-f.points[0].pos[0]) + f.normal[1]*(start_point.pos[1]-f.points[0].pos[1]))/f.normal[2]+f.points[0].pos[2]+params["z"]+self.current_rock.radius
				break
		if np.isnan(start_point.pos[2]):
			Debug.error("Couldn't find a suitable height for the current rock.")
		
		vel=Math.Vector3([self.random_generator.rand()*0.01,self.random_generator.rand()*0.01,params["vz"]])
		if params["random_rocks_ori"]:
			ori = self.random_generator.rand(3)*2*np.pi
		else:
			ori = [0., 0., 0.]
		self.current_rock.setup_kinematics(
			pos = start_point.pos,
			vel = vel,
			angVel = [0., 0., 0.],
			ori = ori
		)
	
	def update_nslaw_params(self):
		if(self.override_rebound_params):
			e=self.override_e
			mu=self.override_mu
			mu_r=self.override_mu_r
		else:
			shapely_point=shapely.geometry.Point(self.current_rock.pos[0:2])
			for i in range(len(self.terrain.soil_params)):	
				if(self.terrain.soil_params[i]["shapely_polygon"].contains(shapely_point)): #NOTE: this could be optimized by avoiding updating mu and e when the rock doesn't change from polygon (when i==0)
					e=self.terrain.soil_params[i]["params"].get("e",self.terrain.default_faces_params["e"])
					mu=self.terrain.soil_params[i]["params"].get("mu",self.terrain.default_faces_params["mu"])
					mu_r=self.terrain.soil_params[i]["params"].get("mu_r",self.terrain.default_faces_params["mu_r"])
					self.terrain.soil_params.insert(0,self.terrain.soil_params.pop(i))	#swap poly_params sequence: put the current one at the first position to increase speed
					break
				#if no polygon found:
				e=self.terrain.default_faces_params["e"]
				mu=self.terrain.default_faces_params["mu"]
				mu_r=self.terrain.default_faces_params["mu_r"]
		nsl = self.mechanicsHdf5Runner._nslaws['lawTerrain']
		nsl.setEn(e)
		nsl.setMu(mu)
		nsl.setMuR(mu_r*self.current_rock.radius)
		Debug.info('update_nslaw_params', e, mu, mu_r*self.current_rock.radius, self.current_rock.pos)
	
	def out_of_bounds_condition(self):
		return self.current_rock.pos[2]<self.terrain.min_height
	
	def reset_trees_contactors(self):
		for i,t in enumerate(self.terrain.trees):
			if not t.active:
				self.mechanicsHdf5Runner.import_object(
					name='tree'+str(i),
					body_class=None,
					shape_class=None,
					face_class=None,
					edge_class=None,
					translation=t._siconos_translation,
					orientation=t._siconos_orientation,
					birth=True
				)
	
	def before_run_tasks(self):
		# PlatRock things
		GenericThreeDSimulation.before_run_tasks(self)
		# Siconos things
		GenericShapeSimulation.before_run_tasks(self)
		# Make references between PlatRock trees and Siconos cylinders:
		# NOTE: this is necessary to enable/disable them.
		for i,t in enumerate(self.terrain.trees):
			t._siconos_static_body_number = self.mechanicsHdf5Runner._static['tree'+str(i)]['number']
			self.terrain._siconos_trees_ids_to_tree_id[t._siconos_static_body_number] = i
	
	def before_rock_launch_tasks(self):
		self.reset_trees_contactors()
		# PlatRock things (add_rock, setup_rock_kinematics):
		GenericThreeDSimulation.before_rock_launch_tasks(self)
		# Siconos things (add_siconos_rock):
		GenericShapeSimulation.before_rock_launch_tasks(self)
		self.update_nslaw_params()

	def rock_propagation_tasks(self):
		if(not self.status=="running"):
			time.sleep(0.1)
			return
		if(self.GUI_enabled):
			if time.time()-self.last_time_computed < self.limit_real_time_dt_interval:
				return
			self.last_time_computed=time.time()
		
		self.current_rock_previous_vel=Math.Vector3(self.current_rock.vel)
		self.mechanicsHdf5Runner._simulation.computeOneStep()


		#Forest:
		contact_points = self.mechanicsHdf5Runner._io.contactPoints(self.mechanicsHdf5Runner._nsds, 1)
		if contact_points is not None:
			inter_id=contact_points[:,22]
			for i in range(inter_id.shape[0]):
				inter = self.mechanicsHdf5Runner._nsds.interaction(int(inter_id[i]))
				if(inter):
					contact_r = cast_Contact5DR(inter.relation())
					static_body_number = contact_r.bodyShapeRecordB.staticBody.number
					if static_body_number is not None and static_body_number!=-1: # -1 stands for terrain, [-2, -3, ..., nbtrees-1] stands for trees
						tree_id = self.terrain._siconos_trees_ids_to_tree_id[static_body_number]
						t = self.terrain.trees[tree_id]
						r = self.current_rock

						xy_contact_point=t.pos+t.dhp/2/100*Math.normalized2(r.pos[0:2]-t.pos)
						self.forest_impact_model.run_3D(r, t, xy_contact_point) #at this stage the current rock r was not updated with siconos outputs
						normal=r.pos.copy()
						normal[0:2]-=t.pos
						normal=normal.normalized()
						self.output.add_contact(r,normal,Outputs.TREE)
						if(self.GUI_enabled):
							t.color=[0.8,0,0]
						# disable the tree for this rock :
						t.active=False
						self.mechanicsHdf5Runner._interman.removeStaticBody(contact_r.bodyShapeRecordB.staticBody)

						# update the rock vel into siconos from the forest impact model output. Note: we make the assuption that angVel is not changed by the tree impact.
						self.current_DS.setVelocityPtr([r.vel[0],r.vel[1],r.vel[2],r.angVel[0],r.angVel[1],r.angVel[2]])

		self.current_rock.pos=Math.Vector3(self.current_DS.q()[:3])
		self.current_rock.vel=Math.Vector3(self.current_DS.velocity()[:3])
		self.current_rock.angVel=Math.Vector3(self.current_DS.velocity()[3:])
		self.current_rock.ori.w=self.current_DS.q()[3]
		self.current_rock.ori.x=self.current_DS.q()[4]
		self.current_rock.ori.y=self.current_DS.q()[5]
		self.current_rock.ori.z=self.current_DS.q()[6]

		self.handle_hdf5_export()

		if self.record_condition():
			#Update terrain parameters sometimes
			self.update_nslaw_params()
			#Check out_of_bounds sometimes
			if self.out_of_bounds_condition() :
				Debug.warning("The rock went outside the terrain !")
				self.current_rock.out_of_bounds=True
				self.current_rock.is_stopped=True
			self.output.add_contact(self.current_rock,Math.Vector3([0,0,0]),Outputs.MOTION)

		if(self.vel_acc_stop_condition()):
			Debug.info("Rock stopped")
			self.current_rock.is_stopped=True
			self.remove_siconos_rock()

		self.mechanicsHdf5Runner._simulation.clearNSDSChangeLog()
		self.mechanicsHdf5Runner._simulation.nextStep()
		self.iter+=1
	
	def get_parameters_verification_report(self):
		report = Report()
		
		#HAS TERRAIN:
		if self.terrain is None:
			report.add_error("The simulation has no terrain.")
		
		#REBOUND PARAMETERS CHECK:
		if self.override_rebound_params:
			report.add_error( "self.override_rebound_params==True is not yet supported in WebUI." )
		report.add_info("Use Siconos physical model.")
		params_descriptors=self.get_terrain_cls().valid_input_soil_geojson_attrs
		
		for i,param_set in enumerate(self.terrain.soil_params):
			if not 'shapely_polygon' in param_set.keys():
				report.add_error( "No polygon found in soil parameter set #%s."%(i) )
			else:
				polygon=param_set["shapely_polygon"]
				if not (isinstance(polygon,shapely.geometry.MultiPolygon) or isinstance(polygon,shapely.geometry.Polygon)):
					report.add_error( "The polygon is invalid in soil parameter set #%s."%(i) )
			for param_desc in params_descriptors.parameters:
				if param_desc.inst_name not in param_set['params'].keys():
					report.add_error( "The parameter name %s is missing in soil parameters set #%s"%(param_desc.inst_name,i) )
				else:
					param_value=param_set['params'][param_desc.inst_name]
					report.check_parameter(param_desc,param_value,location_string="soil parameters set #%s"%(i))
			
		report = self.get_forest_params_verification_report(report)
		return report
