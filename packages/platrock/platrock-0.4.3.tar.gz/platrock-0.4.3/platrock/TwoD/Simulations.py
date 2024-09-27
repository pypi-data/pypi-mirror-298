"""
"""

"""
This module is used by the TwoD model. It is a kind of master module that handles simulations.
"""
#TODO:
# - find a workaround for rebounds that are too small


from . import Objects, Geoms
import platrock.Common.BounceModels as BounceModels
from platrock.Common.TreesGenerators import OneDTreeGenerator
import platrock.Common.Debug as Debug
import platrock.Common.Math as Math
from platrock.Common import Outputs
from platrock.Common.TwoDSimulations import GenericTwoDSimulation
import numpy as np
from platrock.Common.Utils import Report
from platrock.Common.Utils import ParametersDescriptorsSet

import platrock


class Simulation(GenericTwoDSimulation):
	"""
	A TwoD simulation.
	
	"""
	webui_typename="PlatRock 2D"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def add_rock(self):
		self.current_rock=Objects.Rock(
			volume=self.rocks_volumes[self.current_rock_number],
			density=self.rocks_density
		)
	
	def setup_rock_kinematics(self):
		self.current_rock.setup_kinematics(
			x=self.rocks_start_x[self.current_rock_number],
			height=self.rocks_start_z[self.current_rock_number],
			vel=Math.Vector2([self.rocks_vx,self.rocks_vz]),
			angVel=self.rocks_angVel
		)
	
	def before_run_tasks(self):
		super().before_run_tasks()
		if(self.enable_forest and (not self.terrain.forest_available)):
			self.override_forest_params=True
		if(self.override_forest_params and self.override_trees_density==0):
			self.enable_forest=False
	
	def rock_propagation_tasks(self):
		r=self.current_rock
		Debug.info("\nNew rock propagation loop")
		if(abs(r.vel[0])<1e-5):
			r.vel[0]=np.sign(r.vel[0])*1e-5 #the horizontal velocity can't be zero as it would not create a parabolic trajectory
			if(r.vel[0]==0): #if the vel is exactly 0
				r.vel[0]=1e-5
			if len(self.output.get_contacts_types(-1)) == 1 and self.output.get_contacts_types(-1)[0] == Outputs.START :
				self.output.get_contacts_vels(-1)[0,0]=1e-5
			Debug.warning("The rock vel along x is too small (<1e-5), set it to",r.vel[0])
		
		#FOREST=======================================================================================================#
		if(self.enable_forest):
			loop_counter=-1
			rolling = False
			r.force_roll=False
			# Loop on portions of the trajectory. The loop ends only when the rock rebounds on the SOIL 
			while(True):
				#INIT:
				loop_counter+=1
				Debug.info("Start tree loop")
				r.update_flying_direction() #if the previous loop changed the rock propagation direction
				parabola=Geoms.Parabola(r,g=self.gravity)
				Debug.info("Rock parabola:",parabola.A,"*x*x +",parabola.B,"*x +",parabola.C)
				arrow_x=parabola.get_arrow_x_from_gradient(r.current_segment.slope_gradient) #what will be the x coord of the maximal height reached by the rock on this segment ?
				arrow_height=parabola.get_value_at(arrow_x)-r.current_segment.get_z(arrow_x)
	
				#DO WE ROLL OR DO WE FLY ?
				if loop_counter==0: #this means that the rock is currently in contact with the SOIL (no tree, OR not in flight, OR first portion of roll in this segment). Roll can only be triggered in this case.
					if arrow_height < r.radius/10 or r.force_roll:
						Debug.info("Set rolling to True with arrow_x=",arrow_x,"and arrow_height=",arrow_height)
						rolling=True
						self.output.del_contact(-1,-1) #remove the last contact, we will add a rolling contact instead.

				#HORIZONTAL DISTANCE TRAVELLED ON THE CURRENT SEGMENT WITH THE ROLL
				if rolling :
					mu_r = self.override_mu_r if self.override_rebound_params else r.current_segment.mu_r
					AR=BounceModels.Azzoni_Roll(r.vel,mu_r,-r.current_segment.slope,self.gravity,start_pos=r.pos,tan_slope=-r.current_segment.slope_gradient,A=r.A)
					self.output.add_contact(r,r.current_segment.normal,Outputs.ROLL)
					arrival_point=AR.stop_pos
					#Limit the arrival point to the segment extremas
					if arrival_point[0] < r.current_segment.points[0][0]:
						arrival_point=r.current_segment.points[0]
					elif arrival_point[0] > r.current_segment.points[1][0]:
						arrival_point=r.current_segment.points[1]
					else:
						AR.until_stop=True
					arrival_point=Math.Vector2(arrival_point)
					xdist_travel_on_segment=arrival_point[0]-r.pos[0]
				
				#HORIZONTAL DISTANCE TRAVELLED ON THE CURRENT SEGMENT WITH THE PARABOLA
				else:
									#PARABOLA COMPUTATION, STOP CONDITION:
					try:
						freefall_bounce_point,rebound_segment=Geoms.find_next_bounce(self,r,rock_parabola=parabola) #free fall bounce point, previsional bounce point if we don't consider the forest
					except :
						r.out_of_bounds=True
						r.is_stopped=True #just to stop propagation in main loop (Common.Simulations.GenericSimulation.run())
						Debug.info("No intersection could be found, check rock.out_of_bounds to find out what happened.")
						return
					if(r.flying_direction>0):	# The end of the trajectory on the current segment is determined either by the next rebound or by the segment ends.
						xdist_travel_on_segment=min(freefall_bounce_point[0],r.current_segment.points[1][0])-r.pos[0]
					else:
						xdist_travel_on_segment=max(freefall_bounce_point[0],r.current_segment.points[0][0])-r.pos[0]

				#FOREST PARAMETERS OVERRIDES:
				if(self.override_forest_params):
					trees_density=self.override_trees_density
					trees_dhp_std=self.override_trees_dhp_std
					trees_dhp_mean=self.override_trees_dhp_mean
				else:
					trees_density=r.current_segment.trees_density
					trees_dhp_std=r.current_segment.trees_dhp_std
					trees_dhp_mean=r.current_segment.trees_dhp_mean
				if(trees_density>1e-5 and trees_dhp_mean>1e-5 and trees_dhp_std>1e-5):
					dhp=Math.get_random_value_from_gamma_distribution(trees_dhp_mean,trees_dhp_std,self.random_generator)
				else:
					trees_density=0
					dhp=0
				
				#WHAT DISTANCE CAN WE STATISTICALLY TRAVEL ALONG X BEFORE REACHING A TREE ?
				if(trees_density<=1e-5 or dhp<0.01): # avoid zero division
					next_tree_impact_xdist=np.inf
				else:
					#Convert trees_density from tree/ha to tree/m², dhp_mean from cm to m.
					treeGenerator=OneDTreeGenerator(self,treesDensity=trees_density/10000,trees_dhp=trees_dhp_mean/100,dRock=r.radius*2.)
					#next_tree_impact_xdist=((100./np.sqrt(trees_density))**2)/(dhp_mean/100. + r.radius*2.)
					next_tree_impact_xdist=treeGenerator.getOneRandomTreeImpactDistance()
				Debug.info("Next_tree_impact_xdist :",next_tree_impact_xdist)
				
				#WILL THERE BE A TREE-CONTACT BEFORE REACHING THE END OF THIS SEGMENT ? ...
				Debug.info("Comparing abs(xdist_travel_on_segment)=abs(",xdist_travel_on_segment, ") with next_tree_impact_xdist=",next_tree_impact_xdist)
				if(next_tree_impact_xdist<abs(xdist_travel_on_segment)): # then an impact with a tree will hapen before the end of the travel on this segment.
				#... YES! ROLL OR FLY TO THIS POINT IN ANY CASES
					impact_point=Math.Vector2([r.pos[0]+r.flying_direction*next_tree_impact_xdist,0.0]) # set x first
					if rolling:
						AR.until_stop=False #finally the rock will not roll until stop, as there is a tree before.
						impact_point[1]=r.current_segment.get_z(impact_point[0]) # set z
						r.roll(self,AR,impact_point)
					else:
						impact_point[1]=parabola.get_value_at(impact_point[0]) # set z
						impact_height = impact_point[1]-r.current_segment.get_z(impact_point[0])
						r.fly(impact_point,self,r.current_segment)
						#IF THE ROCK FLIES LOW ENOUGH, MODIFY ITS VEL AND STORE THE CONTACT:
						if(impact_height>2): #no rock-tree impact if impact height is too high
							continue #the while(True) loop
					#After roll or fly, do the rock-tree contact:
					self.forest_impact_model.run_2D(r, dhp, self.random_generator.rand(), rolling)
					if rolling :
						self.output.add_contact(r,(1*r.flying_direction,0.),Outputs.ROLL_TREE)
					else :
						self.output.add_contact(r,(1*r.flying_direction,0.),Outputs.TREE)
					Debug.info("Impact with a tree at:",impact_point,", dhp=",dhp,"cm", "output vel is",r.vel)
				#... NO! THERE WILL BE A FREEFLIGHT OR ROLL
				else:
					#ROLL TO THE NEXT SEGMENT OR UNTIL STOP:
					if rolling:
						# as r.current_segment will be modified in r.roll():
						prev_segment_id=r.current_segment.index
						r.roll(self,AR,arrival_point)# note: AR.until_stop have been set earlier
						#if we rolled until out_of_bounds occured. Note that r.is_stopped==True here.
						if r.out_of_bounds :
							self.output.add_contact(r,Math.Vector2([0.,0.]),Outputs.SOIL)
						#handle junction with next segment
						if not r.is_stopped :
							angle_segs=self.terrain.get_angle_between(prev_segment_id, r.current_segment.index) #the slope discontinuity angle
							if abs(angle_segs-np.pi) < 1e-2 : # angle=180° (collinear)
								Debug.info("After roll, collinear segment -> still roll.")
								r.force_roll=True
								self.output.add_contact(r,Math.Vector2([0.,1.]),Outputs.ROLL) # the next loop will be a roll, so this contact will be immediately removed
							elif angle_segs>np.pi:	# angle>180°, just a soil-like contact so that at next loop we will have a flight
								Debug.info("After roll, free fly.")
								self.output.add_contact(r,Math.Vector2([0.,1.]),Outputs.SOIL)
							elif angle_segs>np.pi/2:	# 90°>angle>180°, we have a real contact with the segment, compute the bounce here.
								Debug.info("After roll, contact on soil.")
								self.output.add_contact(r,r.bounce(self,r.current_segment,disable_roughness=True),Outputs.SOIL)
								r.update_flying_direction()
								r.update_current_segment(self.terrain) #the previous r.bounce may have changed the rock vel x-direction. Update the current_segment, knowing that the rock is exactly between two segments.
							else:	# angle<90°, we have a frontal impact, stop the rock.
								Debug.info("After roll, stop rock.")
								r.is_stopped=True
						break #end the infinite loop

					#FLY TO THE NEXT SEGMENT OR THE NEXT SOIL CONTACT
					else:
						#i) the rock will fly until a rebound on the current segment :
						if(rebound_segment.index==r.current_segment.index):
							Debug.info("No tree impact detected until next bounce on soil")
							r.fly(freefall_bounce_point,self,rebound_segment) #fly to the bounce point
							self.output.add_contact(r,r.bounce(self, rebound_segment),Outputs.SOIL) #bounce here
							break	#end the infinite loop
						#ii) the rock will fly to the next segment
						else:
							#do a PORTION of flight, until reaching the next segment
							Debug.info("Fly above the current segment to the begining of the next one")
							if(r.flying_direction>0):
								next_x=r.current_segment.points[1][0]
								next_seg=self.terrain.segments[r.current_segment.index+1]
							else:
								next_x=r.current_segment.points[0][0]
								next_seg=self.terrain.segments[r.current_segment.index-1]
							r.fly(Math.Vector2([next_x,parabola.get_value_at(next_x)]),self,next_seg)
		#/FOREST=======================================================================================================#
		
		#NO FOREST=====================================================================================================#
		else: #no forest :
			r.update_flying_direction() #if the previous loop changed the rock propagation direction
			parabola=Geoms.Parabola(r,g=self.gravity)
			Debug.info("Rock parabola:",parabola.A,"*x*x +",parabola.B,"*x +",parabola.C)
			arrow_x=parabola.get_arrow_x_from_gradient(r.current_segment.slope_gradient) #what will be the x coord of the maximal height reached by the rock on this segment ?
			arrow_height=parabola.get_value_at(arrow_x)-r.current_segment.get_z(arrow_x)
			
			# FLIGHT #
			if arrow_height > r.radius/10 and not r.force_roll : #the arrow is high-enough to do a FLIGHT:
				Debug.info("FLY")
				try:
					bounce_point,rebound_segment=Geoms.find_next_bounce(self,r,parabola) #free fall bounce point, previsional bounce point
				except : #no bounce point have been found...
					r.out_of_bounds=True
					r.is_stopped=True
					Debug.warning("No intersection could be found, maybe the rock went out of terrain bounds ?")
					return
				r.fly(bounce_point,self,rebound_segment)
				if not r.is_stopped :
					#Bounce on the destination segment :
					self.output.add_contact(r,r.bounce(self, rebound_segment),Outputs.SOIL)

			# ROLL #
			else:
				Debug.info("ROLL")
				mu_r = self.override_mu_r if self.override_rebound_params else r.current_segment.mu_r
				AR=BounceModels.Azzoni_Roll(r.vel,mu_r,-r.current_segment.slope,self.gravity,start_pos=r.pos,tan_slope=-r.current_segment.slope_gradient,A=r.A)
				#As we are rolling, replace the last contact recorded by a roll-contact
				self.output.del_contact(-1,-1) #remove the last contact, we will add a rolling contact instead.
				self.output.add_contact(r,r.current_segment.normal,Outputs.ROLL)
				arrival_point=AR.stop_pos
				#Limit the arrival point to the segment extremas
				if arrival_point[0] < r.current_segment.points[0][0]:
					arrival_point=r.current_segment.points[0]
				elif arrival_point[0] > r.current_segment.points[1][0]:
					arrival_point=r.current_segment.points[1]
				else:
					AR.until_stop=True
				arrival_point=Math.Vector2(arrival_point)
				# as r.current_segment will be modified in r.roll()
				prev_segment_id=r.current_segment.index 
				r.roll(self,AR,arrival_point)
				#if we rolled until out_of_bounds occured. Note that r.is_stopped==True here.
				if r.out_of_bounds :
					self.output.add_contact(r,Math.Vector2([0.,0.]),Outputs.SOIL)
				#handle junction with next segment
				r.force_roll=False
				if not r.is_stopped :
					angle_segs=self.terrain.get_angle_between(prev_segment_id, r.current_segment.index) #the slope discontinuity angle
					if abs(angle_segs-np.pi) < 1e-2 : #collinear
						Debug.info("After roll, collinear segment -> still roll.")
						r.force_roll=True
						self.output.add_contact(r,Math.Vector2([0.,1.]),Outputs.ROLL) # the next loop will be a roll, so this contact will be immediately removed
					elif angle_segs>=np.pi :	# angle>180°, just a soil-like contact so that at next loop we will have a flight
						Debug.info("After roll, free fly.")
						self.output.add_contact(r,Math.Vector2([0.,1.]),Outputs.SOIL)
					elif angle_segs>np.pi/2:	# 90°>angle>180°, we have a real contact with the segment, compute the bounce here.
						Debug.info("After roll, contact on soil.")
						self.output.add_contact(r,r.bounce(self,r.current_segment,disable_roughness=True),Outputs.SOIL)
						r.update_flying_direction()
						r.update_current_segment(self.terrain) #the previous r.bounce may have changed the rock vel x-direction. Update the current_segment, knowing that the rock is exactly between two segments.
					else:	# angle<90°, we have a frontal impact, stop the rock.
						Debug.info("After roll, stop rock.")
						r.is_stopped=True
	
	def get_parameters_verification_report(self):
		report = Report()
		
		#HAS TERRAIN:
		if self.terrain is None:
			report.add_error("The simulation has no terrain.")
		
		#REBOUND PARAMETERS CHECK:
		if self.override_rebound_params:
			report.add_info("Segments rebound parameters are globally overriden.")
			if self.override_bounce_model_number in BounceModels.number_to_model_correspondance.keys() :
				BM_cls=BounceModels.number_to_model_correspondance[self.override_bounce_model_number]
				for param_descriptor in BM_cls.valid_input_attrs.parameters:
					param_value=getattr(self,"override_"+param_descriptor.inst_name)
					report.check_parameter(param_descriptor,param_value,location_string="overriden rebound parameters")
			else:
				report.add_error( "The overriden bounce model number is invalid (override_bounce_model_number=%s)."%(self.override_bounce_model_number) )
		else:
			report.add_info("Rebound parameters are handled by segments.")
			for segt in self.terrain.segments:
				if segt.bounce_model_number in BounceModels.number_to_model_correspondance.keys():
					BM_cls=BounceModels.number_to_model_correspondance[segt.bounce_model_number]
					for param_descriptor in BM_cls.valid_input_attrs.parameters:
						param_value=getattr(segt,param_descriptor.inst_name)
						report.check_parameter(param_descriptor,param_value,location_string="segment #%s"%(segt.index))
				else:
					report.add_error( "In segment #%s, the bounce model number is invalid (bounce_model_number=%s)."%(segt.index,segt.bounce_model_number) )
			
		#FOREST PARAMETERS CHECK:
		if self.enable_forest:
			report.add_info("Forest is activated.")
			if self.override_forest_params:
				report.add_info("Segments forest parameters are globally overriden.")
				for param_descriptor in self.forest_impact_model.valid_input_attrs.parameters:
					param_value=getattr(self,"override_"+param_descriptor.inst_name)
					report.check_parameter(param_descriptor,param_value,location_string="overriden forest parameters")
		else:
			report.add_info("Forest is disabled.")
		return report
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
