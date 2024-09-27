"""
"""

"""
This module is used by the ThreeD model. It handles all the Objects types
"""

import numpy as np
from platrock.Common import Utils, BounceModels, Math, Debug
from platrock.Common.ThreeDObjects import GenericThreeDRock, GenericThreeDCheckpoint, GenericThreeDTerrain
import copy

import platrock


class Sphere(GenericThreeDRock):
	"""
	FIXME: DOC
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.I=np.ones(3)*2./5.*self.mass*self.radius**2
		self.bounding_box=Bounding_Box()
		self.verlet_faces_list=[]
		self.verlet_trees_list=[]
		self.terrain_active_contact=None
		self.tree_active_contact=None
		self.VTK_actor=None	#VTK actor for visualization
		self.opacity=1

class Contact(object):
	def __init__(self):
		self.dist=None
		self.rock_force=None
		self.rock_torque=None
		self.rock_pos=None
		self.rock_output_vel=None
		self.rock_output_angVel=None
		self.rock_output_ori=None
	
	def get_storage_copy(self,r):
		c=copy.copy(self)
		c.rock_force=r.force.copy()
		c.rock_torque=r.torque.copy()
		c.rock_pos=r.pos.copy()
		c.rock_output_velocity=r.vel.copy()
		c.rock_output_angVel=r.angVel.copy()
		c.rock_output_ori=copy.copy(r.ori)
		return c

class Rock_terrain_contact(Contact):
	def __init__(self,point,face):
		super().__init__()
		self.point=point	#this is the rock point, not the contact point.
		self.face=face
	
	def get_storage_copy(self, r):
		c=super().get_storage_copy(r)
		#NOTE : the objects below are not copied, only linked
		c.point=self.point
		c.face=self.face
		return c
		

class Rock_tree_contact(Contact):
	def __init__(self,tree):
		super().__init__()
		self.tree=tree
	
	def get_storage_copy(self, r):
		c=super().get_storage_copy(r)
		c.tree_pos=self.tree.pos.copy()
		#NOTE : the object below is not copied, only linked
		c.tree=self.tree
		return c

class Bounding_Box(object):
	def __init__(self):
		self.pos=Math.Vector3([0,0,0])
		self.half_length=0	#set this to 0 so that the Verlet algorithm detect that the bounding sphere has not yet been initialized.
		self.VTK_actor=None
		self.opacity=0.25

class Checkpoint(GenericThreeDCheckpoint):
	pass #nothing to change to the parent class, just declare here for consistency and facilitate eventual future implementations.

class Terrain(GenericThreeDTerrain):
	valid_input_soil_geojson_attrs=Utils.ParametersDescriptorsSet([])
	for bounce_class in BounceModels.number_to_model_correspondance.values():
		valid_input_soil_geojson_attrs+=bounce_class.valid_input_attrs
	
	def __init__(
		self,
		default_faces_params={
			"R_n":0.6,
			"R_t":0.6,
			"roughness":0.1,
			"bounce_model_number":0,
			"phi":30,
			"v_half":2.5,
			"e":0.1,
			"mu":0.8,
			"mu_r":0.5
		},
		*args, **kwargs):
		self.default_faces_params=default_faces_params
		self.faces_xyz_bb=None
		super().__init__(*args, **kwargs)
	