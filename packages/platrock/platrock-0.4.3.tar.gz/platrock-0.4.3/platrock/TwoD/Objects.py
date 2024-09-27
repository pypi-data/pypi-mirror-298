"""
This module handles the objects types needed by the TwoD model.
"""

#FIXME : allow to set default segments parameters from the launch script (as in 3D).

import numpy as np
import platrock.Common.Debug as Debug
import copy,sys
import platrock.Common.Math as Math
import platrock.Common.TwoDObjects
from platrock.Common import Outputs
from platrock.Common.Utils import ParametersDescriptorsSet
import platrock.Common.BounceModels as BounceModels

class Rock(platrock.Common.TwoDObjects.GenericTwoDRock):
	"""
	A falling rock.
	
	Args:
		x (float): initial position along the x axis. Note that the coordinates system used is the one after the terrain is eventually cleaned, shifted and reversed.
		height (float): initial height relative to the terrain
	
	Attributes:
		vel (:class:`Common.Math.Vector2` [float,float]): velocity along x,z
		angVel (float): angular velocity
		volume (float): volume
		density (float): density
		I (float): inertia, autocomputed if not given
		pos (:class:`~platrock.Common.Math.Vector2`): position along x,z, autocomputed
		radius (float): radius, autocomputed
		mass (float): mass, autocomputed
		A (float): an intermediate result of the Azzoni Roll, automatically precomputed
		v_square (float): an intermediate value computed into the Azzoni Roll
		force_roll (bool): a flag set/used into the roll algorithm to handle roll along two colinear segments
		is_stopped (boolean): flag triggered when the stopping condition is reached
		current_segment (:class:`Segment`): the current segment that is vertically under the rock
		flying_direction (int): -1 if the rock is moving towards -x, +1 if the rock is moving towards +x
		color (list [float,float,float]): the rock RGB color, each compound being between 0. and 1., autocomputed
		out_of_bounds (bool): set to true during the simulation if the rock went out of the terrain
	"""
	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.A = self.mass/(self.mass+self.I/self.radius**2) # see Azzoni et al. 1995
		self.v_square=0 #needed by the rolling aglorithm
		self.force_roll=False
			
	def update_flying_direction(self):
		"""
		Deduce and update the :attr:`flying_direction` from the velocity.
		"""
		self.flying_direction=int(np.sign(self.vel[0]))
		Debug.info("Rock direction is set to",self.flying_direction)
	
	def move(self,arrival_point,s,segment):
		"""
		Actually move the rock by updating its :attr:`pos`. The current simulation and arrival segment must be given as they are usually already computed at this stage.
		
		Note:
			This method also handles the rock stop condition, it has in charge to set :attr:`is_stopped`.
		
		Args:
			arrival_point (:class:`~platrock.Common.Math.Vector2`): the new position along x,z
			s (:class:`~TwoD.Simulations.Simulation`): the current simulation, needed to access its output
			segment (:class:`Segment`): the segment that is vertically under the rock after the move
		"""
		self.pos=arrival_point
		self.update_current_segment(segment)
	
	def fly(self,arrival_point,s,segment):
		"""
		Apply a fly movement to the rock, it will update the position and the velocity of the rock.
		
		Args:
			arrival_point (:class:`~platrock.Common.Math.Vector2`): the new position along x,z
			s (:class:`~TwoD.Simulations.Simulation`): the current simulation, needed to access its output
			segment (:class:`Segment`): the segment that is vertically under the rock after the move
		"""
		#update velocity regarding the  arrival point :
		self.vel[1]=-s.gravity*(arrival_point[0]-self.pos[0])/self.vel[0] + self.vel[1]
		Debug.info("Fly to",arrival_point,",new vel is",self.vel)
		self.move(arrival_point,s,segment)
	
	def roll(self,s,azzoni_roll,arrival_point):
		"""
		Apply a roll movement to the rock, it will update the position, velocity and angVel of the rock.
		
		Args:
			s (:class:`~TwoD.Simulations.Simulation`): the current simulation, needed to access its output
			azzoni_roll (:class:`~platrock.Common.BounceModels.Azzoni_Roll`): the instanciated roll model as it contains necessary attributes and methods
			arrival_point (:class:`~platrock.Common.Math.Vector2`): the new position along x,z
		"""
		Debug.info("Roll to ",arrival_point)
		if(azzoni_roll.until_stop):
			self.vel*=0
			self.angVel*=0
			self.move(arrival_point,s,self.current_segment)
			Debug.info("ROCK STOPPED")
			self.is_stopped=True
		else:
			self.vel=azzoni_roll.get_vel(arrival_point)
			self.angVel = Math.Vector1(- self.flying_direction * self.vel.norm()/self.radius)
			if self.flying_direction>0 and arrival_point[0]>=self.current_segment.points[1][0] :
				next_seg_id=self.current_segment.index+1
			elif self.flying_direction<0 and arrival_point[0]<=self.current_segment.points[0][0] :
				next_seg_id=self.current_segment.index-1
			else: next_seg_id=self.current_segment.index
			if next_seg_id<0 or next_seg_id>len(s.terrain.segments)-1 :
				self.out_of_bounds=True
				self.is_stopped=True
				next_segment = self.current_segment
			else:
				next_segment = s.terrain.segments[next_seg_id] 
				
			self.move(arrival_point,s,next_segment)
	
	def bounce(self,s,segment,disable_roughness=False):
		"""
		Apply a bounce from :py:mod:`platrock.Common.BounceModels` to the rock, it will update the velocity and angVel of the rock.
		
		Args:
			s (:class:`~TwoD.Simulations.Simulation`): the current simulation, needed to access its output
			segment (:class:`Segment`): the segment that is vertically under the rock
			disable_roughness (bool): use this to tell the bounce model not to apply the terrain roughness
		"""
		if(s.override_rebound_params):
			bounce_model_number=s.override_bounce_model_number
		else:
			bounce_model_number=segment.bounce_model_number
		bounce_model=s.number_to_bounce_model_instance[bounce_model_number]
		bounce_model.run(self,segment,disable_roughness)
		return bounce_model.updated_normal

class Segment(platrock.Common.TwoDObjects.GenericSegment):
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
	
	valid_input_attrs=ParametersDescriptorsSet([])
	"""Describes the available soil attributes, they are a concatenation of all bounce models parameters."""
	for bounce_class in BounceModels.number_to_model_correspondance.values():
		valid_input_attrs+=bounce_class.valid_input_attrs
	valid_input_attrs+=BounceModels.Toe_Tree.valid_input_attrs
	del bounce_class #avoid temp variable to show up in the doc

class Terrain(platrock.Common.TwoDObjects.GenericTwoDTerrain):
	"""
	A 2D terrain made of segments.
	
	Args:
		file (string):
		
	Attributes:
		segments (list): the successive :class:`Segment` forming the terrain
		rebound_models_available (list): A list of available bounce models numbers regarding the per-segment input parameters given, automatically filled.
		forest_available (bool): whether the forest is available in the terrain regarding the per-segment input parameters given, automatically set.
	"""
	
	valid_input_attrs=Segment.valid_input_attrs
	
	def __init__(self, *args, **kwargs):
		self.rebound_models_available=[]#A list of available rebound models regarding the per-segment input parameters given. Modified by check_segments_parameters_consistency() method.
		super().__init__(*args, **kwargs)

	def check_segments_parameters_consistency(self):
		"""
			Analyze the segments parameters and checks their consistency/availability. :attr:`forest_available` and :attr:`rebound_models_available` are here.
		"""
		super().check_segments_forest_parameters_consistency()
		s=self.segments[0] #all the segments has the same data, use the first one to list them below
		HAS_bounce_model_number=s.bounce_model_number is not None
		HAS_roughness=s.roughness is not None
		HAS_R_t=s.R_t is not None
		HAS_R_n=s.R_n is not None
		HAS_v_half=s.v_half is not None
		HAS_phi=s.phi is not None
		if(HAS_bounce_model_number):
			if(HAS_roughness and HAS_R_t and HAS_R_n):
				self.rebound_models_available+=[0,1]
			if(HAS_v_half and HAS_phi):
				self.rebound_models_available+=[2]
			bounce_model_numbers=[s.bounce_model_number for s in self.segments]
			USE_classical = 0 in bounce_model_numbers
			USE_pfeiffer = 1 in bounce_model_numbers
			USE_bourrier = 2 in bounce_model_numbers
			if( USE_classical and (0 not in self.rebound_models_available)):
				raise ValueError('At least one segment "rebound_model" parameter has been set to 0(=Classical) but the corresponding parameters were not specified (roughness, R_n, R_t)')
			if( USE_pfeiffer and (1 not in self.rebound_models_available)):
				raise ValueError('At least one segment "rebound_model" parameter has been set to 1(=Pfeiffer) but the corresponding parameters were not specified (roughness, R_n, R_t)')
			if( USE_bourrier and (2 not in self.rebound_models_available)):
				raise ValueError('At least one segment "rebound_model" parameter has been set to 2(=Bourrier) but the corresponding parameters were not specified (roughness, R_t, v_half, phi)')
		
class Checkpoint(platrock.Common.TwoDObjects.GenericTwoDCheckpoint):
	pass #nothing to change to the parent class, just declare here for consistency and facilitate eventual future implementations.










