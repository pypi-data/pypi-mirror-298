"""
This module is used to store output data in an optimized hdf5 file.
"""

import h5py
import numpy as np
import platrock.Common.Debug as Debug

# from platrock.Common.TwoDSimulations import GenericTwoDSimulation #this makes a circular import error when doing "import platrock.TwoDShape.Simulations" from pure python.
# from platrock.Common.ThreeDSimulations import GenericThreeDSimulation

float_type = np.float32

#Contact types :
START=0
"""The rock initial position"""
SOIL=1
"""Rock-soil contact"""
TREE=2
"""Rock-tree contact"""
ROLL_TREE=3
"""Contact with a tree while rolling"""
ROLL=4		#
"""Rolling-friction"""
STOP=5
"""Rock stop position"""
OUT=6
"""Rock out of terrain"""
FLY=7
"""For :class:`ThreeD.Postprocessings.Postprocessing` only, to describe a fly-over-raster-cell"""
MOTION=8	#used by ShapedSimulations 
"""For :class:`ShapedSimulations` only, to track the motion of the rocks (don't really track contacts)"""


class Output(object):
	"""
	Captures rocks contacts data for a whole simulation and organize them in a structured way. Getters functions helps to retrieve and select data from the strucure. Hdf5 file export is also supported.
	
	Args:
		s (a :class:`Simulation` instance): will be :attr:`_s` attribute.
		
	Attributes:
		_s (a :class:`Simulation` instance): binds to the simulation to retrieve informations from it.
		contacts_slices (dict of slices): helper dict that links fields name to the corresponding columns in the :attr:`contacts` output array
		checkpoints (list of :class:`checkpoint`): the list of checkpoints, binded to the simulations checkpoints.
		volumes (:class:`numpy.ndarray`): the 1D array of rocks volumes
		densities (:class:`numpy.ndarray`): the 1D array of rocks densities
		inertias (:class:`numpy.ndarray`): the 1D or 3D array of rocks inertias
		contacts (list of :class:`numpy.ndarray`): the list of contacts for all rocks, each rock is a numpy array with first dimension length equals the number of contacts, second dimension equals the number of fields recorded (see :attr:`contact_slices`).
	"""
	def __init__(self,s):
		self._s=s
		self._rocks_counter=0
		if "GenericTwoDSimulation" in [parent.__name__ for parent in self._s.__class__.__mro__]:
			self._ndim=2
			self.contacts_slices = {
				"types":slice(0,1),
				"rock_pos":slice(1,3),
				"rock_output_vels":slice(3,5),
				"rock_output_angVels":slice(5,6),
				"normals":slice(6,8)
			}
		elif "GenericThreeDSimulation" in [parent.__name__ for parent in self._s.__class__.__mro__]:
			self._ndim=3
			self.contacts_slices = {
				"types":slice(0,1),
				"rock_pos":slice(1,4),
				"rock_output_vels":slice(4,7),
				"rock_output_angVels":slice(7,10),
				"normals":slice(10,13)
			}
		self._contacts_fields_length=0
		for cs in self.contacts_slices.values():
			self._contacts_fields_length+=cs.stop-cs.start
		
		self.checkpoints=None #this is a list directly exported from the "update_checkpoints" function
		self.volumes=np.empty([self._s.nb_rocks],dtype=float_type)
		self.densities=np.empty([self._s.nb_rocks],dtype=float_type)
		if self._ndim==2:
			self.inertias=np.empty([self._s.nb_rocks],dtype=float_type)
		else:
			self.inertias=np.empty([self._s.nb_rocks,3,3],dtype=float_type) #3X3 matrix
		self.contacts=[]

	def add_rock(self,r):
		"""
		Add a rock with no contacts to the output. This is triggered by the :meth:`~Common.Simulations.GenericSimulation.before_rock_launch_tasks` functions. Stores rock quantities such a volume, density, inertia...
		
		Args:
			r (:class:`Rock`): instanciated rock
		"""
		self.volumes[self._rocks_counter]=float_type(r.volume)
		self.densities[self._rocks_counter]=float_type(r.density)
		if self._ndim==2:
			self.inertias[self._rocks_counter]=float_type(r.I)
		elif r.I.shape==(3,): #diagonal
			self.inertias[self._rocks_counter]=float_type(np.identity(3)*r.I)
		elif r.I.shape==(3,3): #matrix
			self.inertias[self._rocks_counter]=r.I
		else:
			Debug.error("This rock has an invalid inertia shape:",r.I)
		self.contacts.append(np.empty([0,self._contacts_fields_length],dtype=float_type))
		self._rocks_counter+=1
	
	def add_contact(self,r,normal,type_):
		"""
		Add a contact to the last rock added to the output. This is triggered by the :meth:`~Common.Simulations.GenericSimulation.rock_propagation_tasks` functions at each contact. It will store contact-related infos, such as position, velocity...
		
		Args:
			r (:class:`Rock`) instanciated rock
			normal (:class:`platrock.Common.Math.Vector2` | :class:`Common.Math.Vector3`) the contact normal (branch vector)
			type_ (int): one of the contact type (ex: :attr:`SOIL`)
		"""
		new_contact_data=np.concatenate((
			[type_],
			r.pos,
			r.vel,
			r.angVel,
			normal
		)).astype(float_type)
		self.contacts[-1]=np.append(self.contacts[-1],[new_contact_data],axis=0)
	
	def del_contact(self,rock_id,contact_id):
		"""
		Sometimes a contact must be deleted for a given rock.
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to remove a contact
			contact_id (int): if equals -1, remove the last contact, else remove the contact at this index in :attr:`contacts`
		"""
		if contact_id == -1:
			self.contacts[rock_id]=self.contacts[rock_id][:contact_id]
		else:
			self.contacts[rock_id]=np.append(self.contacts[rock_id][:contact_id] , self.contacts[rock_id][contact_id+1:])
	
	def get_contacts_field(self,rock_id,field):
		"""
		From a rock number, retrive all contact data corresponding to the field name (see :attr:`contacts_slices`)
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to retrieve infos
			field (string): the data to retrieve (see keys of :attr:`contacts_slices`)
		
		Returns:
			:class:`numpy.ndarray`
		"""
		return self.contacts[rock_id][:,self.contacts_slices[field]]
	
	def get_contacts_pos(self,rock_id):
		"""
		From a rock number, retrive all contacts positions.
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to retrieve infos
		
		Returns:
			:class:`numpy.ndarray`
		"""
		return self.get_contacts_field(rock_id,"rock_pos")
	
	def get_contacts_vels(self,rock_id):
		"""
		From a rock number, retrive all contacts velocities.
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to retrieve infos
		
		Returns:
			:class:`numpy.ndarray`
		"""
		return self.get_contacts_field(rock_id,"rock_output_vels")
	
	def get_contacts_angVels(self,rock_id):
		"""
		From a rock number, retrive all contacts angVels.
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to retrieve infos
		
		Returns:
			:class:`numpy.ndarray`
		"""
		if(self._ndim==2):
			return self.get_contacts_field(rock_id,"rock_output_angVels")[:,0]
		else:
			return self.get_contacts_field(rock_id,"rock_output_angVels")
		
	def get_contacts_types(self,rock_id):
		"""
		From a rock number, retrive all contacts types.
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to retrieve infos
		
		Returns:
			:class:`numpy.ndarray`
		"""
		return self.get_contacts_field(rock_id,"types")[:,0]
	
	def get_contacts_normals(self,rock_id):
		"""
		From a rock number, retrive all contacts normals.
		
		Args:
			rock_id (int): the rock index in :attr:`contacts` from which to retrieve infos
		
		Returns:
			:class:`numpy.ndarray`
		"""
		return self.get_contacts_field(rock_id,"normals")

	def write_to_h5(self,filename):
		"""
		Export this output to a hdf5 file.
		
		Note:
			It is advised to use `hdf-compass <https://support.hdfgroup.org/projects/compass/download.html>`_ to read hdf5 files. Use :code:`sudo apt install hdf-compass` on debian-based distros such as Ubuntu.
		
		Note:
			Here is the hdf5 file structure created::
				
				# hdf5-file/
				# ├── rocks/
				# |   ├── start_data
				# |   └── contacts/
				# |       ├── 0 (contacts of rock n°0)
				# |       ├── ..
				# |       └── nb_rocks
				# └── checkpoints/
				#     ├── x_0 (x position of checkpoint 0)
				#     ├── x_1
				#     └── x_N
		"""
		with h5py.File(filename, "w") as f:
			f.create_group("rocks")
			f.create_group("rocks/contacts")
			f.create_group("checkpoints")
			
			#ROCKS START DATA:
			#prepare data:
			
			if self._ndim==2:
				inertias = self.inertias.reshape([self._s.nb_rocks,1])
			else :
				inertias = self.inertias.reshape([self._s.nb_rocks,9])
			start_data=np.concatenate((
				self.volumes.reshape([self._s.nb_rocks,1]),
				self.densities.reshape([self._s.nb_rocks,1]),
				inertias
			),axis=1).astype(float_type)
			#write to file:
			f.create_dataset("rocks/start_data",data=start_data)
			#add attributes that embed the links between start_data columns and data types
			f["rocks/start_data"].attrs["volumes"]=0
			f["rocks/start_data"].attrs["densities"]=1
			if(self._ndim==2):
				f["rocks/start_data"].attrs["inertias"]=2
			else:
				f["rocks/start_data"].attrs["inertias"]=[2,10]
			
			#ROCKS CONTACTS DATA:
			#loop on "rocks"
			for i in range(len(self.contacts)):
				#write the contacts of the rock i
				f.create_dataset("rocks/contacts/"+str(i),data=self.contacts[i].astype(float_type))
			#add attributes that embed the links between contacts data columns and data types
			for k in self.contacts_slices.keys():
				f["rocks/contacts"].attrs[k]=[self.contacts_slices[k].start,self.contacts_slices[k].stop-1]
			
			#CHECKPOINTS:
			if(self._s.checkpoints is not None):
				for c_id,c in enumerate(self.checkpoints):
					data_len=len(c.rocks_ids)
					if(data_len):
						if self._ndim == 2 :
							angVels=np.asarray(c.angVels).reshape([data_len,1])
							heights2D_or_pos3D=np.asarray(c.heights).reshape([data_len,1])
						else:
							angVels=np.asarray(c.angVels)
							heights2D_or_pos3D=np.asarray(c.pos)
						chckpt_data=np.concatenate((
							np.asarray(c.rocks_ids).reshape([data_len,1]),
							heights2D_or_pos3D,
							np.asarray(c.vels),
							angVels,
						),axis=1)
					else:
						chckpt_data=np.array([])
					f.create_dataset("checkpoints/"+str(c_id),data=chckpt_data.astype(float_type))
					f["checkpoints"].attrs["rocks_ids"]=[0,0]
					if(self._ndim==2):
						f["checkpoints"].attrs["heights"]=[1,1]
						f["checkpoints"].attrs["vels"]=[2,3]
						f["checkpoints"].attrs["angVels"]=[4,4]
					else:
						f["checkpoints"].attrs["pos"]=[1,3]
						f["checkpoints"].attrs["vels"]=[4,6]
						f["checkpoints"].attrs["angVels"]=[7,9]
				
