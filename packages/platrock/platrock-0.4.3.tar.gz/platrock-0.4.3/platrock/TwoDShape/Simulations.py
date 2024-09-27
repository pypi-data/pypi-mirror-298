"""
"""

from platrock.Common.TwoDSimulations import GenericTwoDSimulation
from platrock.Common.ShapeSimulations import GenericShapeSimulation
from platrock.Common.TimeSteppedSimulations import GenericTimeSteppedSimulation
from platrock.Common import Math, Outputs, Utils, Debug
from platrock.Common.TreesGenerators import OneDTreeGenerator
from . import Objects
import numpy as np

from siconos.mechanics.collision.tools import Contactor
import siconos.numerics as sn

import platrock

class Simulation(GenericTwoDSimulation, GenericShapeSimulation, GenericTimeSteppedSimulation):
	webui_typename="PlatRock 2D-Shape"
	valid_rocks_start_params=GenericTwoDSimulation.valid_rocks_start_params
	valid_rocks_start_params+=Utils.ParametersDescriptorsSet([
			["random_rocks_ori",	"random_rocks_ori",		"Random orientation",				bool,		True],
			["rocks_ori",			"rocks_ori",			"Orientation (degrees)",			int,		0,			359,	0],
	])
	if platrock.web_ui :
		valid_rocks_start_params+=Utils.ParametersDescriptorsSet([
			["StringChoice", ["rocks_shape", "shape"],	"rocks_shape",	"Rocks shape",	'Ellipse', [sc.__name__ for sc in Objects.Rock.__subclasses__()]]
		])
	
	def __init__(self, dt = 0.001, *args, **kwargs):
		GenericTimeSteppedSimulation.__init__(self, dt = dt)
		GenericTwoDSimulation.__init__(self, *args,**kwargs)
		GenericShapeSimulation.__init__(self)
		
		# For tree impact distance computation:
		self.last_rock_zone=None
		self.prev_step_tree_impact=False
		self.next_tree_impact_xdist=None
		self.next_tree_dhp=None
		self.next_tree_impact_rockx=None #the rock x position when the next_tree_impact_xdist was computed.
	
	def out_of_bounds_condition(self):
		return self.current_rock.pos[0]<self.terrain.segments[0].points[0][0] or \
		self.current_rock.pos[0]>self.terrain.segments[-1].points[1][0] or \
		self.current_rock.pos[1]<self.terrain.get_z_range()[0]
	
	def setup_siconos(self):
		return GenericShapeSimulation.setup_siconos(self, sn.SICONOS_ROLLING_FRICTION_2D_NSGS)
		
	def add_terrain(self):
		terrain_points=self.terrain.get_points()
		terrain_min_z=terrain_points[:,1].min()-10
		for seg in self.terrain.segments:
			seg.siconos_points=np.array([
				[seg.points[0][0],seg.points[0][1]],
				[seg.points[1][0],seg.points[1][1]],
				[seg.points[1][0],terrain_min_z],
				[seg.points[0][0],terrain_min_z]
			])
			self.mechanicsHdf5Runner.add_convex_shape(
				'Seg'+str(seg.index),
				seg.siconos_points,
				outsideMargin=self.outside_margin,
				insideMargin=self.inside_margin,
				avoid_internal_edge_contact=True
			)
			self.mechanicsHdf5Runner.add_object(
				'seg'+str(seg.index),
				[
					Contactor(
						'Seg'+str(seg.index),
						collision_group=seg.index+1
					)
				],
				translation = [0,0]
			)

			if self.override_rebound_params:
				e=self.override_e
				mu=self.override_mu
				mu_r=self.override_mu_r
			else:
				e=seg.e
				mu=seg.mu
				mu_r=seg.mu_r
			seg.adopted_base_mu_r = mu_r # NOTE needed at each rock launch to set mu_r as a function of the rock equivalent radius
			self.mechanicsHdf5Runner.add_Newton_impact_rolling_friction_nsl(
				'lawSeg'+str(seg.index),
				e=e,
				mu=mu,
				mu_r=mu_r,
				collision_group1=seg.index+1,
				collision_group2=0
			)
	
	def add_rock(self):
		# Check whether we should change the rock shape.
		if hasattr(self.current_rock, 'nb_diff_shapes') and self.current_rock.nb_diff_shapes>1 and self.current_rock_number>0 :
			# The following line gives an array of rocks number for which we should generate a new shape.
			shapes_changes_rocks_nb = np.where((np.arange(0,self.nb_rocks)%(self.nb_rocks/self.current_rock.nb_diff_shapes)).astype(int) == 0)[0]
			if self.current_rock_number in shapes_changes_rocks_nb:
				# Actually change the rock shape
				self.current_rock.generate()
				Debug.info('Generate new rock at rock nb ',self.current_rock_number,'. ','New vertices: ',self.current_rock.vertices)
		self.current_rock.density=self.rocks_density
		self.current_rock.set_volume(self.rocks_volumes[self.current_rock_number])
	
	def setup_rock_kinematics(self):
		if(self.random_rocks_ori):
			ori=self.random_generator.rand()*np.pi*2
		else:
			ori=np.radians(self.rocks_ori)
		self.current_rock.setup_kinematics(
			x=self.rocks_start_x[self.current_rock_number],
			height=self.rocks_start_z[self.current_rock_number],
			vel=Math.Vector2([self.rocks_vx,self.rocks_vz]),
			angVel=self.rocks_angVel,
			ori = ori
		)
	
	def before_run_tasks(self):
		# PlatRock things
		GenericTwoDSimulation.before_run_tasks(self)
		# Siconos things
		GenericShapeSimulation.before_run_tasks(self)

	def before_rock_launch_tasks(self):
		# PlatRock things (add_rock, setup_rock_kinematics):
		GenericTwoDSimulation.before_rock_launch_tasks(self)
		# Siconos things (add_siconos_rock):
		GenericShapeSimulation.before_rock_launch_tasks(self)
		for seg in self.terrain.segments:
			nsl = self.mechanicsHdf5Runner._nslaws['lawSeg'+str(seg.index)]
			nsl.setMuR(seg.adopted_base_mu_r*self.current_rock.radius)
	
	def rock_propagation_tasks(self):
		prev_velx = self.current_DS.velocity()[0]
		self.current_rock_previous_vel=self.current_rock.vel[:]
		self.mechanicsHdf5Runner._simulation.computeOneStep()
		
		pos=self.current_DS.q()
		vel=self.current_DS.velocity()
		self.current_rock.pos=Math.Vector2(pos[0:2])
		self.current_rock.ori=Math.Vector1([pos[2]])
		self.current_rock.vel=Math.Vector2(vel[0:2])
		self.current_rock.angVel=Math.Vector1(vel[2])
		
		if(self.enable_forest):
			if (self.prev_step_tree_impact):
				# Record the rock velocity if a tree impact occured at previous step.
				# NOTE: we delay this record to reflect the velocity after a potential contact with the soil that would occur just after the tree contact.
				# NOTE: the tree contact may not be the last recorded, so search it.
				# NOTE: don't allow two successive tree contacts
				self.prev_step_tree_impact = False
				for c_idx,contact_type in list(enumerate(self.output.get_contacts_types(-1)))[::-1]:
					if (contact_type == Outputs.TREE):
						self.output.contacts[-1][c_idx, self.output.contacts_slices["rock_output_vels"]] = np.copy(self.current_rock.vel)
						break
			else:
				zone=self.terrain.get_zone_at_x(self.current_rock.pos[0])
				if(not zone):
					pass
				else:
					if(	not self.last_rock_zone or 
						not (self.last_rock_zone is zone) or #use "is" for object comparison by reference 
						prev_velx*self.current_rock.vel[0]<0 or #the rock changed its direction along X
						not self.next_tree_impact_xdist
						):
						self.last_rock_zone=zone
						# Compute new next_tree_impact_xdist
						if(self.override_forest_params):
							trees_density=self.override_trees_density
							trees_dhp_std=self.override_trees_dhp_std
							trees_dhp_mean=self.override_trees_dhp_mean
						else:
							trees_density=zone["params"]["trees_density"]
							trees_dhp_std=zone["params"]["trees_dhp_std"]
							trees_dhp_mean=zone["params"]["trees_dhp_mean"]
						#WHAT DISTANCE CAN WE STATISTICALLY TRAVEL ALONG X BEFORE REACHING A TREE ?
						if(trees_density<=1e-5 or trees_dhp_mean<0.01): # avoid zero division
							self.next_tree_impact_xdist=np.inf
						else:
							#Convert trees_density from tree/ha to tree/m², dhp_mean from cm to m.
							treeGenerator=OneDTreeGenerator(self,treesDensity=trees_density/10000,trees_dhp=trees_dhp_mean/100,dRock=self.current_rock.radius*2.)
							self.next_tree_impact_xdist=treeGenerator.getOneRandomTreeImpactDistance()
							self.next_tree_impact_rockx=self.current_rock.pos[0]
							self.next_tree_dhp=Math.get_random_value_from_gamma_distribution(trees_dhp_mean,trees_dhp_std,self.random_generator)
						# print("New next tree dist",self.next_tree_impact_xdist)
					if(abs(self.current_rock.pos[0]-self.next_tree_impact_rockx)>self.next_tree_impact_xdist): #impact with tree
						self.forest_impact_model.run_2D(self.current_rock, self.next_tree_dhp, self.random_generator.rand())
						# vx=vx*np.sign(self.current_rock.vel[0])
						# toe_output_vel=Math.Vector2([vx,vz])
						#Linear interpolation of velocity norm between PlatRock input vel and Toe's input one :
						# out_vel_norm=self.current_rock.vel.norm()*toe_output_vel.norm()/self.forest_impact_model.last_computed_data["input_vel"]
						# toe_output_vel=toe_output_vel.normalized()*out_vel_norm
						# self.current_rock.vel[0]=toe_output_vel[0]
						# self.current_rock.vel[1]=toe_output_vel[1]
						self.output.add_contact(self.current_rock,(np.sign(self.current_rock.vel[0]),0.),Outputs.TREE)
						self.current_DS.setVelocityPtr([self.current_rock.vel[0],self.current_rock.vel[1],self.current_DS.velocity()[2]]) #NOTE: change velocity into siconos
						self.next_tree_impact_xdist=None #trigger new tree distance calculation, and resets next_tree_impact_rockx
						self.prev_step_tree_impact = True #trigger vel change in output after next siconos iteration
		
		self.handle_hdf5_export()

		if self.vel_acc_stop_condition():
			Debug.info("Rock stopped")
			self.current_rock.is_stopped=True
			self.remove_siconos_rock()
		
		#Record trajectory
		if self.record_condition():
			#Check out_of_bounds sometimes
			if self.out_of_bounds_condition() :
				self.current_rock.out_of_bounds=True
				self.current_rock.is_stopped=True
			self.output.add_contact(self.current_rock,Math.Vector2([0,0]),Outputs.MOTION)

		self.mechanicsHdf5Runner._simulation.clearNSDSChangeLog()
		self.mechanicsHdf5Runner._simulation.nextStep()
		
				
	def after_all_tasks(self,*args,**kwargs):
		super(Simulation, self).after_all_tasks(*args,**kwargs)
		self.mechanicsHdf5Runner.__exit__(None, None, None)

	def get_parameters_verification_report(self):
		report = Utils.Report()
		
		#HAS TERRAIN:
		if self.terrain is None:
			report.add_error("The simulation has no terrain.")
		#REBOUND PARAMETERS CHECK:
		if self.override_rebound_params:
			report.add_info("Segments rebound parameters are globally overriden.")
			for param_descriptor in self.terrain.valid_input_attrs.parameters:
				param_value=getattr(self,"override_"+param_descriptor.inst_name)
				report.check_parameter(param_descriptor,param_value,location_string="overriden rebound parameters")
		else:
			report.add_info("Rebound parameters are handled by segments.")
			for segt in self.terrain.segments:
				for param_descriptor in self.terrain.valid_input_attrs.parameters:
					param_value=getattr(segt,param_descriptor.inst_name)
					report.check_parameter(param_descriptor,param_value,location_string="segment #%s"%(segt.index))
			
		#FOREST PARAMETERS CHECK:
		#FIXME: to do later when forest is implemented.
		return report














