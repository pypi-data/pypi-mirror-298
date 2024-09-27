import numpy as np
import sys, math
from platrock.Common.Utils import ParametersDescriptorsSet
import platrock.Common.PyUtils as PyUtils
import platrock.Common.Math as Math
import platrock.Common.Debug as Debug
import platrock.Common.ColorPalettes as cp
from platrock.TwoD import Geoms

class GenericRock(object):
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
		current_segment (:class:`GenericSegment`): the current segment that is vertically under the rock
		flying_direction (int): -1 if the rock is moving towards -x, +1 if the rock is moving towards +x
		color (list [float,float,float]): the rock RGB color, each compound being between 0. and 1., autocomputed
		out_of_bounds (bool): set to true during the simulation if the rock went out of the terrain
	"""

	def __init__(self, volume=None, density=None, I=None):
		self.volume=volume
		self.density=density
		self.radius = (3.*self.volume/np.pi/4.)**(1./3.)
		self.mass = self.volume*self.density
		if I is None:
			self.I = 2./5.*self.mass*self.radius**2
		else:
			self.I = I
		self.pos=None
		self.vel=None
		self.angVel=None
		self.is_stopped=None
		self.out_of_bounds=False
		self.color=np.random.rand(3).tolist()
	
	@classmethod
	def _new_retro_compat_template(cls):
		return cls(volume=1., density=2500., I=10000.)

	def setup_kinematics(self): #implemented in childs
		return

class GenericCheckpoint(object):
	"""
	A checkpoint along the terrain. Checkpoints data are post-computed from all contacts of all rocks.
	
	Args:
		rocks (list [:class:`Rock`, ...]): all rocks that passed through the checkpoint
		heights (list [float, ...]): all heights at which the rocks passed through the checkpoint
		vels (list [[vx1,vz1], [vx2,vz2], ...]): all velocities at which the rocks passed through the checkpoint
		angVels (list [float, ...]): all angVels at which the rocks passed through the checkpoint
	"""
	def init_data(self):
		self.vels=[]
		self.angVels=[]
		self.rocks_ids=[]

class GenericTerrain(object):
	@classmethod
	def get_parent_module(cls):
		for ancestor in cls.__mro__:
			if 'platrock.' in ancestor.__module__:
				return sys.modules[ancestor.__module__]
		raise TypeError("Couldn't find the terrain parent module. Did you make an exotic platrock import or subclassing ?")

