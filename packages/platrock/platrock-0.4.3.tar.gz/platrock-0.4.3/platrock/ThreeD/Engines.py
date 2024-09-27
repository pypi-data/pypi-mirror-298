"""
"""

"""
This module handles all the engines (the core) of the ThreeD code.
TODO : add rock-terrain and rock-tree Cython functions.
"""

from platrock.Common import Debug, Math, Outputs, ThreeDToolbox
from platrock.Common.Utils import ParametersDescriptorsSet
import numpy as np
from . import Objects
import quaternion, shapely
import copy
import types


# from siconos.mechanics.collision.bullet import *

class Engine(object):
	"""
	"Abstract" class for all engines. Each engine has a run() method which is run at each "iter_every" iteration. Engines instances must be stored in :attr:`ThreeD.Simulations.Simulation.Engines`.
	
	Args:
		dead (bool): if True, the engine will not be ran
		iter_every (int): run the engine each iter_every timesteps
	"""
	def __init__(self,iter_every=1,use_cython=True):
		self.dead=False
		self.iter_every=iter_every
		self.use_cython=use_cython


class Verlet_update(Engine):
	"""
	Update the rocks faces (:attr:`ThreeD.Objects.Rock.verlet_faces_list`) and trees (:attr:`ThreeD.Objects.Rock.verlet_trees_list`) neighbours lists.
	
	Args:
		dist_factor (float): the verlet distance factor (dist_factor * rock_radius = verlet distance). Values must be >1, but values >5 are highly recommanded.If dist_factor==1, the verlet algorithm will be unefficient.
		
	"""
	def __init__(self,dist_factor=5,**kwargs):
		super(Verlet_update,self).__init__(**kwargs)
		self.dist_factor=dist_factor
	
	def run(self, *args, **kwargs):
		if(self.use_cython):
			self.run = types.MethodType(ThreeDToolbox.verlet_run,self)
		else:
			self.run = self.run_python
		return self.run(*args, **kwargs)

	def run_python(self,s):
		r=s.current_rock
		if(not((r.pos-r.radius*1.1<r.bounding_box.pos-r.bounding_box.half_length).any() or (r.pos+r.radius*1.1>r.bounding_box.pos+r.bounding_box.half_length).any())): #if the rock stays inside the box
			return
		r.bounding_box.half_length=self.dist_factor*r.radius
		r.bounding_box.pos[:]=r.pos[:]
		
		# ROCK - TERRAIN verlet list :
		r.verlet_faces_list=[]	#initialize the list
		mins_check_outside = (r.bounding_box.pos+r.bounding_box.half_length<s.terrain.faces_xyz_bb[:,0::2]).any(axis=1)
		maxs_check_outside = (r.bounding_box.pos-r.bounding_box.half_length>s.terrain.faces_xyz_bb[:,1::2]).any(axis=1)
		inside_mask = np.logical_not(np.logical_or(mins_check_outside, maxs_check_outside))
		r.verlet_faces_list=s.terrain.faces[inside_mask].tolist()
		
		if(s.enable_forest):
			r.verlet_trees_list=[]
			# ROCK - TREES verlet list :
			dists=((s.terrain.trees_as_array[:,0:2] - r.pos[0:2])**2).sum(axis=1)-(s.terrain.trees_as_array[:,2]/2)**2# all (rock centroid) - (trees) squared distances. NOTE: trees_as_array[:,2] are the dhp per trees
			active_indices=np.where(dists<(r.bounding_box.half_length)**2)[0]	#indices of trees composing the verlet list
			r.verlet_trees_list=np.asarray(s.terrain.trees)[active_indices]
			#Debug.info("len(verlet_trees_list) =",len(r.verlet_trees_list))

class Contacts_detector(Engine):
	"""
	FIXME:DOC
	Append (real, geometrical) contacts into :attr:`ThreeD.Objects.Rock.terrain_active_contacts` dict. Rock-Face goes into :attr:`terrain_active_contacts["terrain"]<ThreeD.Objects.Rock.>`  and Rock-Tree contacts goes into :attr:`terrain_active_contacts["tree"]<ThreeD.Objects.Rock.terrain_active_contacts>` .
	"""
	def __init__(self,**kwargs):
		super(Contacts_detector,self).__init__(**kwargs)
	
	def run(self, *args, **kwargs):
		if(self.use_cython):
			self.run = types.MethodType(ThreeDToolbox.contacts_detector_run,self)
		else:
			self.run = self.run_python
		return self.run(*args, **kwargs)

	def run_python(self,s):
		# ROCK-TERRAIN :
		r=s.current_rock
		r.terrain_active_contact=None
		face_candidate=None
		face_candidate_dist=np.inf
		#for rp in r.points:
		rp=r.points[0] #for a Object.Sphere there is a unique point
		for tf in r.verlet_faces_list:
			dist=tf.normal.dot(rp.pos-tf.points[0].pos)-r.radius	# first pass : point-plane distance. Negative dist <=> interpenetration.
			if(dist>0.): # no penetration with the plan : no contact possible
				continue
			if(r.vel.dot(tf.normal)>0): #if the rock goes appart from the face. This check was added with the edge and wedge contact detection: edge and wedge detection algorithms could lead to select a face the rock is going appart from.
				continue
			# We now search the nearest distance between the sphere and the triangle. 3 possibilities: surface contact, edge contact, vertex contact
			if(tf.is_point_inside_3D(rp)):
				#we are sure that the contact is on the face surface
				if(dist<face_candidate_dist):
					#this is currently the best candidate
					face_candidate=tf
					face_candidate_dist=dist
				continue 	#as the contact is on the face surface, it is not on an edge or on a vertex. So continue to the next face
			# We now search an edge contact
			found_edge_contact=False
			for i in range(-1,2):
				branch=rp.pos-tf.points[i].pos
				edge=tf.points[i+1].pos-tf.points[i].pos
				proj_coef=branch.dot(edge)/(branch.norm()**2)
				if(proj_coef>1 or proj_coef<0):continue #the projection of the sphere center on the edge is outside the edge
				proj=edge*proj_coef
				dist=(branch-proj).norm()-r.radius
				if(dist<face_candidate_dist and dist<0):
					#this is currently the best candidate
					face_candidate=tf
					face_candidate_dist=dist
					found_edge_contact=True
			if(found_edge_contact):continue	#as the contact is on an edge, it is not on a vertex. So continue to the next face
			# We now search a vertex contact
			for i in range(0,3):
				dist=(tf.points[i].pos-rp.pos).norm()-r.radius
				if(dist<face_candidate_dist and dist<0):
					#this is currently the best candidate
					face_candidate=tf
					face_candidate_dist=dist
		if(face_candidate_dist<0):	#the default value for face_candidate_dist is +infinity, see above.
			r.terrain_active_contact=Objects.Rock_terrain_contact(rp,face_candidate)
			r.terrain_active_contact.dist=face_candidate_dist
		
		# ROCK - TREES :
		if(s.enable_forest):
			r.tree_active_contact=None
			for t in r.verlet_trees_list:
				if(t.active):
					dist=Math.norm2(r.pos[0:2]-t.pos)-r.radius-t.dhp/2./100	#negative dist <=> interpenetration
					if(dist<0.):
						r.tree_active_contact=Objects.Rock_tree_contact(t)
						r.tree_active_contact.dist=dist
		
		

class Nscd_integrator(Engine):
	"""
	FIXME : doc
	"""
	def __init__(self,**kwargs):
		super(Nscd_integrator,self).__init__(**kwargs)
	
	def run(self, *args, **kwargs):
		if(self.use_cython):
			self.run = types.MethodType(ThreeDToolbox.nscd_integrator_run,self)
		else:
			self.run = self.run_python
		return self.run(*args, **kwargs)

	def run_python(self,s):
		r=s.current_rock
		r.pos+=r.vel*s.dt - 0.5*s.gravity*s.dt**2
		r.vel-=s.gravity*s.dt
		if(s.GUI_enabled):
			#/!\ NOTE this rotational integration scheme is only valid for spheres
			r.ori=quaternion.from_rotation_vector(r.angVel*s.dt)*r.ori
			r.ori=r.ori.normalized()
		r.update_members_pos()
		if(r.pos[2]<s.terrain.min_height):
				Debug.warning("The rock went outside the terrain !")
				r.out_of_bounds=True
				r.is_stopped=True

class Rock_terrain_nscd_basic_contact(Engine):
	"""
	FIXME : doc
	"""
	def __init__(self,**kwargs):
		super(Rock_terrain_nscd_basic_contact,self).__init__(**kwargs)
	def run(self,s):
		r=s.current_rock
		if(r.terrain_active_contact):
			f=r.terrain_active_contact.face
			if(s.override_rebound_params):
				bounce_model_number=s.override_bounce_model_number
			else:
				bounce_model_number=f.bounce_model_number
			BM=s.number_to_bounce_model_instance[bounce_model_number]
			BM.run(r,f)
			cp=r.pos-r.radius*f.normal
			#Push the sphere outside the face along the z axis. Use the z axis and not face.normal as the latter would cause bugs in Posprocessings.
			r.pos[2]+=-(f.normal[0]*(cp[0]-f.points[0].pos[0]) + f.normal[1]*(cp[1]-f.points[0].pos[1]))/f.normal[2]+f.points[0].pos[2]-cp[2]+0.01*r.radius
			s.output.add_contact(r,BM.updated_normal,Outputs.SOIL)

class Rock_tree_nscd_basic_contact(Engine):
	"""
	FIXME : doc
	"""
	def __init__(self,**kwargs):
		super(Rock_tree_nscd_basic_contact,self).__init__(**kwargs)
	def run(self,s):
		r=s.current_rock
		if(not r.terrain_active_contact and r.tree_active_contact):
			Debug.info("Rock-tree contact !")
			t=r.tree_active_contact.tree
			xy_contact_point=t.pos+t.dhp/2/100*Math.normalized2(r.pos[0:2]-t.pos)
			s.forest_impact_model.run_3D(r, t, xy_contact_point)
			
			normal=r.pos.copy()
			normal[0:2]-=t.pos
			normal=normal.normalized()
			s.output.add_contact(r,normal,Outputs.TREE)
			t.active=False
			if(s.GUI_enabled):
				t.color=[0.8,0,0]
			
class Snapshooter(Engine):
	def __init__(self,filename="snap_",**kwargs):
		super(Snapshooter,self).__init__(**kwargs)
		self.filename=filename
		self.ndone=0
	def run(self,s):
		s.GUI.take_snapshot(self.filename+str(self.ndone).rjust(6,"0")+".png")
		self.ndone+=1
		
class Time_stepper(Engine):
	def __init__(self,safety_coefficient=0.1,**kwargs):
		super(Time_stepper,self).__init__(**kwargs)
		self.safety_coefficient=safety_coefficient
	def run(self,s):
		s.dt=self.safety_coefficient*s.current_rock.radius/(s.current_rock.vel.norm())
		s.dt=min(s.dt,0.1)
		#Debug.warning("New time step:",s.dt)
