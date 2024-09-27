"""
This module is the placeholder for all :class:`BounceModel` of PlatRock physical models. It is used by TwoD and ThreeD (non-siconos).
"""

import numpy as np
from . import Debug,Math
import os, requests, h5py
from scipy import spatial
from platrock.Common.Utils import ParametersDescriptorsSet
from platrock import DATA_DIR

class BounceModel(object):
	"""
	The parent class of every rock-soil bounce models. The table below represents the bounce-models dependency to the soil parameters. The soil parameters of the terrain elements (segments or faces) must be set according to this table. Similarly, the input files (csv or geojson) must be consistent with this table. Note that the parameters are case-sensitive.
	
	.. _bounce_params:

	+------------------+---------------------------+-----------------+------------+------------+------------+--------------+------------+
	|                  |:attr:`bounce_model_number`|:attr:`roughness`|:attr:`mu_r`|:attr:`R_n` | :attr:`R_t`|:attr:`v_half`|:attr:`phi` |
	+------------------+---------------------------+-----------------+------------+------------+------------+--------------+------------+
	|Classical         |            *              |        *        |     *      |     *      |     *      |              |            |
	+------------------+---------------------------+-----------------+------------+------------+------------+--------------+------------+
	|Pfeiffer          |            *              |        *        |     *      |     *      |     *      |              |            |
	+------------------+---------------------------+-----------------+------------+------------+------------+--------------+------------+
	|Bourrier          |            *              |        *        |     *      |            |     *      |      *       |     *      |
	+------------------+---------------------------+-----------------+------------+------------+------------+--------------+------------+
	
	Attributes:
		updated_normal (:class:`~Common.Math.Vector2` || :class:`~Common.Math.Vector3`): the segment (2D) or face (3D) rotated normal used to emulate roughness.
		simulation (a child of :class:`~Common.Simulations.GenericSimulation`, optional): the parent simulation, as the bounce models needs it to get its type and random generator. It should be a child class of :class:`~Common.Simulations.GenericSimulation`.
	"""
	
	
	valid_input_attrs=ParametersDescriptorsSet([
		["roughness",							"roughness",			"Roughness",					float,	0,		10.		,0.1],
		[["bounce_model_number","bounce_mod"],	"bounce_model_number",	"Rebound model",				int,	0,		2		,0],
		["mu_r",								"mu_r",					"μ<sub>r</sub>",				float,	0,		100		,0.2],
		["R_t",									"R_t",					"R<sub>t</sub>",				float,	0,		0.95	,0.05],
	])
	"""The set of parameters needed by all bounce models."""
	
	def __init__(self,simulation=None):
		self.updated_normal=None
		self.simulation=simulation
	
	def set_updated_normal(self,*args,**kwargs):
		"""
		Set :attr:`updated_normal` from the soil element normal, the rock velocity and the soil roughness.
		
		Note:
			This method is self-overriden by :meth:`set_updated_normal2D` or :meth:`set_updated_normal3D` at its first call, depending on the simulation type.
			On previous implementations the binding was made in "__init__" but it caused jsonpickle to don't load "set_updated_normal" function at all.
			Reason:Jsonpickle doesn't run __init__ on load, but rather :
			- restore attributes from json file
			- "restore" methods from the existing class in memory
			
			So in the previous implementation "set_updated_normal" was not an attribute, and neither a member function of BounceModel.
		
		Args:
			*args: see :meth:`set_updated_normal2D` or :meth:`set_updated_normal3D`
			**kwargs: see :meth:`set_updated_normal2D` or :meth:`set_updated_normal3D`
			
		"""
		if "GenericTwoDSimulation" in [parent.__name__ for parent in self.simulation.__class__.__mro__]:
		# if("TwoD" in self.simulation.get_parent_module().__name__):
			self.set_updated_normal=self.set_updated_normal2D
			self.check_output_vel=self.check_output_vel_2D
		else:
			self.set_updated_normal=self.set_updated_normal3D
			self.check_output_vel=self.check_output_vel_3D
		self.set_updated_normal(*args,**kwargs)
	
	def set_updated_normal2D(self,rock,normal,roughness):
		"""
		Set :attr:`updated_normal` from the segment normal, the rock propagation direction and the soil roughness.
		
		Args:
			rock (:class:`~TwoD.Objects.Rock`): the current rock
			normal (:class:`~Common.Math.Vector2`): the current segment normal
			roughness (float): the current segment roughness
		"""
		roughness_angle=self.simulation.random_generator.rand()*np.arctan(roughness/rock.radius)
		roughness_angle*=np.sign(rock.vel.cross(normal))
		self.updated_normal=normal.rotated(roughness_angle)
		if(self.updated_normal[1]<0.01):	#AVOID THE ROUGHNESS TO CAUSE SLOPE HIGHER THAN 90° OR LESS THAN -90°.
			Debug.info("Roughness caused slope higher than 90 or lower than -90 with normal =",self.updated_normal)
			self.updated_normal[1]=0.01		#Set the z component of the normal=0.01
			self.updated_normal[0]=np.sqrt(1-0.01**2)*np.sign(self.updated_normal[0])	#ajust the x component according to the normalization condition
		Debug.info("updated_normal =",self.updated_normal)
		
	def set_updated_normal3D(self,rock,normal,roughness):
		"""
		Set :attr:`updated_normal` from the face normal, the rock propagation direction and the soil roughness.
		
		Args:
			rock (:class:`~TwoD.Objects.Rock`): the current rock
			normal (:class:`~Common.Math.Vector3`): the current segment normal
			roughness (float): the current segment roughness
		"""
		nd=(rock.vel-rock.vel.dot(normal)*normal).normalized() #local CS, velocity direction
		nt=(nd.cross(normal)).normalized() #local CS, direction orthogonal to velocity
		roughness_angle=self.simulation.random_generator.rand()*np.arctan(roughness/rock.radius)
		braking_ratio=self.simulation.random_generator.rand()
		deviation_ratio=np.sign(self.simulation.random_generator.rand()-0.5)*(1-braking_ratio)
		self.updated_normal=normal.rotated(roughness_angle*braking_ratio,nt)
		self.updated_normal=self.updated_normal.rotated(roughness_angle*deviation_ratio,nd)
		#FIXME: can the output vel be "inside" the terrain with that ?
	
	def get_velocity_decomposed(self,v):
		"""
		From the rock velocity in GCS, get the decomposed velocity in local CS (:math:`v_{n}`, :math:`v_t`).
		
		Args:
			v (:class:`~Common.Math.Vector2` || :class:`~Common.Math.Vector3`): input velocity
		
		Returns:
			list[:math:`v_n`, :math:`v_t`]: the normal and tangential velocities in local CS.
		"""
		vn = v.dot(self.updated_normal)*self.updated_normal
		return [vn,v-vn]
	
	def check_output_vel_2D(self,r,f):
		"""
		Checks whether the rock velocity after rebound is valid, and the rocks doens't go down inside the terrain.
		
		Args:
			r (:class:`TwoD.Objects.Rock`): the current rock
			f (:class:`TwoD.Objects.Segment`): the segment on which the rock bounces
		"""
		if(r.vel.cross(f.branch)>-1e-10):
			direction=np.sign(r.vel[0])
			v_norm=r.vel.norm()
			angle = np.pi/180 if direction>0 else np.pi*(1-1/180)
			r.vel=f.branch.rotated(angle).normalized()*v_norm
			self.updated_normal=Math.Vector2([0,0]) #updated_normal is no longer meaningful and difficult to compute for complex rebound models -> disable it.
			Debug.info("Output vel is not valid (inside terrain), modify it to",r.vel)
	
	def check_output_vel_3D(self,r,f):
		"""
		Warning:
			Not implemented.
		"""
		pass


class Classical(BounceModel):
	"""
	Classical :math:`R_n, R_t` bounce model type.
	"""
	
	valid_input_attrs = BounceModel.valid_input_attrs+ParametersDescriptorsSet([
		["R_n",								"R_n",					"R<sub>n</sub>",				float,	0,		0.95,	0.15],
	])
	"""The set of parameters needed by the Classical bounce model."""
	
	def __init__(self,*args):
		super(Classical, self).__init__(*args)

	def run(self,r,f,disable_roughness=False):
		"""
		Runs the bounce model:
		
		#. randomly compute the local slope angle
		#. compute the rock velocity in the local slope coordinate system
		#. apply :math:`R_n` and :math:`R_t` to the local velocity
		#. finally rotate back the velocity into the global coordinates and set it to the rock.
		
		Args:
			r (:class:`TwoD.Objects.Rock` || :class:`ThreeD.Objects.Rock`): the rock that bounces
			f (:class:`TwoD.Objects.Segment` || :class:`ThreeD.Objects.Face`): the terrain element on which the rock bounces
			disable_roughness (bool, optional): disables the :meth:`~BounceModel.set_updated_normal` function
		"""
		if(self.simulation.override_rebound_params):
			roughness=self.simulation.override_roughness
			R_n=self.simulation.override_R_n
			R_t=self.simulation.override_R_t
		else:
			roughness=f.roughness
			R_n=f.R_n
			R_t=f.R_t
		if(disable_roughness):
			roughness=0
		
		#APPLY REBOUND :
		Debug.info("CLASSICAL REBOUND on",f)
		self.set_updated_normal(r,f.normal,roughness)
		Vn, Vt = self.get_velocity_decomposed(r.vel)
		Debug.info("Old vel:",r.vel, "Vn,Vt=",Vn,Vt)
		r.vel=-Vn*R_n+Vt*R_t
		Debug.info("New vel:",r.vel)
		self.check_output_vel(r,f)

class Pfeiffer(BounceModel):
	"""
	Pfeiffer bounce model type (see [Pfeiffer1989]).
	"""
	
	valid_input_attrs = Classical.valid_input_attrs
	"""The set of parameters needed by the Pfeiffer bounce model."""
	
	def __init__(self,*args):
		super(Pfeiffer, self).__init__(*args)

	def run(self,r,f,disable_roughness=False):
		"""
		Runs the bounce model:
		
		#. randomly compute the local slope angle
		#. compute the rock velocity in the local slope coordinate system
		#. compute the friction function and the scaling factor
		#. modify the velocity
		#. finally rotate back the velocity into the global coordinates and set it to the rock.
		
		Args:
			r (:class:`TwoD.Objects.Rock` || :class:`ThreeD.Objects.Rock`): the rock that bounces
			f (:class:`TwoD.Objects.Segment` || :class:`ThreeD.Objects.Face`): the terrain element on which the rock bounces
			disable_roughness (bool, optional): disables the :meth:`~BounceModel.set_updated_normal` function
		"""
		
		#SET PARAMS :
		if(self.simulation.override_rebound_params):
			roughness=self.simulation.override_roughness
			R_n=self.simulation.override_R_n
			R_t=self.simulation.override_R_t
		else:
			roughness=f.roughness
			R_n=f.R_n
			R_t=f.R_t
		if(disable_roughness):
			roughness=0
		
		#APPLY REBOUND :
		Debug.info("PFEIFFER REBOUND on",f)
		self.set_updated_normal(r,f.normal,roughness)
		Vn, Vt = self.get_velocity_decomposed(r.vel)
		
		Ff=R_t+(1.-R_t)/ ((((Vt.norm()-r.angVel.norm()*r.radius)/6.096)**2) +1.2)	#Friction function 6.096=const (vitesse)
		SF=R_t/ ((Vn.norm()/(76.2*R_n))**2+1.)	#Scaling factor
		
		Vn=-Vn.normalized()*Vn.norm()*R_n/(1.+(Vn.norm()/9.144)**2)
		Vt=Vt.normalized()*np.sqrt( ( r.radius**2*(r.I*r.angVel.norm()**2+r.mass*Vt.norm()**2)*Ff*SF ) / ( r.I+r.mass*r.radius**2 ) )
		
		r.vel=Vn+Vt
		r.angVel=self.updated_normal.cross(Vt)   /   r.radius
		Debug.info("New vel:",r.vel)
		Debug.info("New angVel:",r.angVel)
		self.check_output_vel(r,f)

class Bourrier(BounceModel):
	"""
	Bourrier bounce model type (see [Bourrier2011]).
	"""
	
	valid_input_attrs = BounceModel.valid_input_attrs+ParametersDescriptorsSet([
		["phi",								"phi",					"φ",							float,	0,		40,		20],
		["v_half",							"v_half",				"V<sub>1/2</sub>",				float,	0,		50,		10],
	])
	"""The set of parameters needed by the Bourrier bounce model."""
	
	def __init__(self,*args):
		super(Bourrier, self).__init__(*args)

	def run(self,r,f,disable_roughness=False):
		"""
		See [Bourrier2011].
		"""
		
		#SET PARAMS :
		if(self.simulation.override_rebound_params):
			roughness=self.simulation.override_roughness
			R_t=self.simulation.override_R_t
			v_half=self.simulation.override_v_half
			phi=self.simulation.override_phi
		else:
			roughness=f.roughness
			R_t=f.R_t
			v_half=f.v_half
			phi=f.phi
		if(disable_roughness):
			roughness=0
		
		#APPLY REBOUND :
		Debug.info("BOURRIER REBOUND on",f)
		self.set_updated_normal(r,f.normal,roughness)
		Vn, Vt = self.get_velocity_decomposed(r.vel)
		
		#FIXME: compute Vn.norm() and Vt.norm() once for perfomance improvement.
		R_n = v_half/(abs(Vn.norm())+v_half)
		psi = np.degrees(np.arctan((2.*(R_t*Vt.norm()+r.radius*R_t*r.angVel.norm()))/(7.*Vn.norm()*(1.+R_n))))
		if (abs(psi)<phi):
			Debug.info("Adhesion bounce")
			a,b=(5./7.)*R_t*Vt.norm(), (2./7.)*R_t*r.radius*r.angVel.norm() #intermediate computation
			angVel = (b-a)/r.radius
			r.angVel = angVel * Vt.cross(self.updated_normal)/Vt.norm()
			Vt = Vt/Vt.norm()*(a-b)
			Vn = -R_n*Vn
		else:
			Debug.info("Sliding bounce")
			angVel = -(5./2.)*(1.+R_n)*Vn.norm()/r.radius + R_t*r.angVel.norm()
			r.angVel = angVel * Vt.cross(self.updated_normal)/Vt.norm()
			Vt = Vt/Vt.norm() * ( R_t*Vt.norm() + np.tan(np.radians(phi))*(1.+R_n)*Vn.norm() )
			Vn = -R_n*Vn
		r.vel=Vn+Vt
		Debug.info("New vel:",r.vel)
		self.check_output_vel(r,f)


number_to_model_correspondance={0:Classical, 1:Pfeiffer, 2:Bourrier}
"""
A dictionnary that allows to link between the rebound model numbers and the corresponding class.

0: :class:`Classical`
1: :class:`Pfeiffer`
2: :class:`Bourrier`
"""


class Toe_Tree():
	valid_input_attrs=ParametersDescriptorsSet([
		[["trees_density","density"],		"trees_density",		"Trees density  (trees/ha)",	float,	0,		5000,	200],
		[["trees_dhp_mean","dhp_mean"],		"trees_dhp_mean",		"Mean trees ⌀ (cm)",			float,	5,		200,	30 ],
		[["trees_dhp_std","dhp_std"],		"trees_dhp_std",		"σ(trees ⌀)  (cm)",				float,	0.01,	1000,	10 ]
	])
	"""The set of parameters needed by the Toe rock-tree bounce model.
	
	Attributes:
		input_sequence (list): the ordered list of parameters in Toe dem abacus output
		weight_sequence (list): the priority of the parameters when searching a value in the abacus, higher to lower
		toe_array (numpy.ndarray): stores the abacus data in a numpy array for fast multi-dimensional search
		last_computed_data (dict): stores the last computed output properties for access from the outside
	"""
	
	def __init__(self):
		self.input_sequence=["vel","vol","ecc","dbh","ang","vx","vy","vz"]
		self.weight_sequence=["vel","vol","ang","ecc","dbh","vx","vy","vz"]	#FIXME: check this sequence
		self.last_computed_data={}
		self.toe_array=None
		# self.__init_toe_array__()
	
	def __init_toe_array__(self):
		vels=[5., 10., 15., 20., 25., 30.]
		script_dir = os.path.realpath(__file__).rsplit("/",1)[0]
		self.toe_array=np.empty([0,8])	#cols 0->4 are parameters given by input_sequence, cols 5->7 are outputs [vx,vy,vz]
		for vi in range(len(vels)):
			input=np.genfromtxt(script_dir+"/Toe_2018/result"+str(vels[vi])+".txt",skip_header=1)
			input=np.delete(input,[5,6],axis=1) #remove the useless columns (input vels)
			self.toe_array=np.append(self.toe_array,input,axis=0)
		#to sort the array lines we need a "structured view" of it, see https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column and https://docs.scipy.org/doc/numpy/user/basics.rec.html
		toe_structured_view=self.toe_array.view({"names":self.input_sequence,'formats':['float']*len(self.input_sequence)})
		toe_structured_view.sort(order=self.weight_sequence, axis=0)

	def get_output_vel(self,vel=None,vol=None,ecc=None,dbh=None,ang=None):
		"""
		Search in the abacus data array and retuns the nearest value.
		
		Args:
			vel (float): the input rock velocity norm
			vol (float): the volume of the rock
			ecc (float): the input rock eccentricity
			dbh (float): the tree diameter
			ang (float): the angle formed by the rock velocity and the horizontal plane
			
		Returns:
			:class:`numpy.ndarray`: the rock output velocities :math:`v_x, v_y, v_z`.
		"""
		if(self.toe_array is None):
			self.__init_toe_array__()
		#start with the whole array
		sliced_toe_array=self.toe_array.copy()
		dbh*=0.01 #platrock dbh is in cm, while Toe_2018 is in m.
		for key in self.weight_sequence[:-3]:
			col=self.input_sequence.index(key)	#get the current column index
			real_value=locals()[key]			#get the input value
			id_min=np.argmin(abs(sliced_toe_array[:,col]-real_value))
			id_max=len(sliced_toe_array)-np.argmin(abs(sliced_toe_array[::-1,col]-real_value)) -1
			sliced_toe_array=sliced_toe_array[id_min:id_max+1,:] #narrow the slice at each loop
		Debug.info("Toe model with parameters:",sliced_toe_array[0,0:5])
		self.last_computed_data["output_vel_xyz"]=sliced_toe_array[0,-3:]
		self.last_computed_data["input_vel"]=sliced_toe_array[0,0]
		self.last_computed_data["input_vol"]=sliced_toe_array[0,1]
		self.last_computed_data["input_ecc"]=sliced_toe_array[0,2]
		self.last_computed_data["input_dbh"]=sliced_toe_array[0,3]
		self.last_computed_data["input_ang"]=sliced_toe_array[0,4]
		return self.last_computed_data["output_vel_xyz"]
	
	def run_3D(self, r, t, xy_contact_point):
		vxy_rock=Math.Vector2(r.vel[0:2])
		ecc_axis=Math.Vector2([-vxy_rock[1],vxy_rock[0]]).normalized() #the normed axis, orthogonal to vxy, on which the eccentricity is measured from the contact point and vxy
		ecc=(xy_contact_point-t.pos).dot(ecc_axis)/(t.dhp/2./100)	#eccentricity, from -1 to 1
		ang=np.sign(r.vel[2])*abs(np.degrees(np.arctan(r.vel[2]/vxy_rock.norm()))) # the vertical incident angle.
		angle=np.arctan2(vxy_rock[1],vxy_rock[0])	#the signed angle between the rock xy velocity and the +x axis. NOTE: arctan2:=arctan2(y,x)
		input_rock_vel_norm=r.vel.norm()
		r.vel[:] = self.get_output_vel(
			r.vel.norm(),
			r.volume,
			abs(ecc), # We use abs(ecc) as the DEM model is symetric, see the line below for ecc<0.
			t.dhp,
			ang
		) # The output vel here is expressed in Toe's C.S.
		if(ecc<0):r.vel[1]*=-1
		r.vel[0:2]=Math.rotated2(r.vel[0:2],angle) #rotate the vel to translate from Toe's C.S to our global C.S.
		r.vel=r.vel.normalized()*input_rock_vel_norm*r.vel.norm()/self.last_computed_data["input_vel"] #linear interpolation of velocity norm between PlatRock input vel and Toe's input one.

class Toe_Tree_2022():
	data_file_url = 'https://entrepot.recherche.data.gouv.fr/api/access/datafile/:persistentId?persistentId=doi:10.57745/FY4IZI'
	valid_input_attrs=ParametersDescriptorsSet([
		[["trees_density","density"],		"trees_density",		"Trees density  (trees/ha)",	float,	0,		5000,	200],
		[["trees_dhp_mean","dhp_mean"],		"trees_dhp_mean",		"Mean trees ⌀ (cm)",			float,	5,		200,	30 ],
		[["trees_dhp_std","dhp_std"],		"trees_dhp_std",		"σ(trees ⌀)  (cm)",				float,	0.01,	1000,	10 ]
	])
	"""The set of parameters needed by the Toe rock-tree bounce model."""
	params_weights = [1, 1, 1, 1, 1, 1]
	raw_data_col_offset = 1
	raw_data = None
	conv_tab = None
	cKDTree = None
	max_dist = 10000

	def __init__(self):
		self.data_file = None
		if Toe_Tree_2022.raw_data is None or Toe_Tree_2022.cKDTree is None or Toe_Tree_2022.conv_tab is None :
			self.__generate_cKDTree__()
		self.last_computed_data={}
	
	def __get_data_file__(self, force_dl=False):
		self.data_file = DATA_DIR+'Rock_impacts_on_tree_2022.hdf5'
		# Eventually grab the file from data.gouv.fr:
		if (not os.path.isfile(self.data_file) or force_dl):
			os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
			dl_file = requests.get(Toe_Tree_2022.data_file_url, allow_redirects=True)
			with open(self.data_file, 'wb') as f:
				f.write(dl_file.content)
		
	def __load_data__(self):
		if self.data_file is None:
			self.__get_data_file__()
		# Convert hdf5 file to numpy array:
		with h5py.File(self.data_file,"r") as f:
			data = f["data"][:]
		Toe_Tree_2022.raw_data = data[:,Toe_Tree_2022.raw_data_col_offset:]
	
	def __generate_cKDTree__(self):
		if Toe_Tree_2022.raw_data is None:
			self.__load_data__()
		params_len = len(Toe_Tree_2022.params_weights)
		dataknn = np.zeros((Toe_Tree_2022.raw_data.shape[0],params_len))
		conv_tab = np.zeros((3,params_len))
		for i in range(0,params_len):
			conv_tab[0,i] = np.mean(Toe_Tree_2022.raw_data[:,i])
			conv_tab[1,i] = np.std(Toe_Tree_2022.raw_data[:,i])
			conv_tab[2,i] = Toe_Tree_2022.params_weights[i]
			dataknn[:,i] = conv_tab[2,i]*((Toe_Tree_2022.raw_data[:,i]-conv_tab[0,i])/conv_tab[1,i])
		Toe_Tree_2022.conv_tab = conv_tab
		Toe_Tree_2022.cKDTree = spatial.cKDTree(dataknn,balanced_tree=True)

	def get_index(self, inputs):
		if Toe_Tree_2022.cKDTree is None:
			self.__generate_cKDTree__()
		conv_tab = Toe_Tree_2022.conv_tab
		params = list(conv_tab[2,:]*(inputs-conv_tab[0,:])/conv_tab[1,:])
		dist,index=Toe_Tree_2022.cKDTree.query(
			params,
			k=1,
			p=1,
			distance_upper_bound=Toe_Tree_2022.max_dist
		)
		return index
	
	def get_output_vel(self,vel=None,vol=None,ecc=None,dbh=None,ang=None,hi=None):
		index = self.get_index([vel ,vol ,ecc ,dbh ,ang ,hi])
		out_data = Toe_Tree_2022.raw_data[index]
		self.last_computed_data["output_vel_xyz"]=out_data[len(Toe_Tree_2022.params_weights):]
		self.last_computed_data["input_vel"]=out_data[0]
		self.last_computed_data["input_vol"]=out_data[1]
		self.last_computed_data["input_ecc"]=out_data[2]
		self.last_computed_data["input_dbh"]=out_data[3]
		self.last_computed_data["input_ang"]=out_data[4]
		self.last_computed_data["input_hi"]=out_data[5]
		return self.last_computed_data["output_vel_xyz"]
	
	def run_2D(self, rock, dhp, ecc, rolling=False):
		vx, vy, vz = self.get_output_vel(
			vel = rock.vel.norm(),
			vol = rock.volume,
			ecc = ecc,
			dbh = dhp,
			ang = np.sign(rock.vel[1])*abs(np.degrees(np.arctan(rock.vel[1]/rock.vel[0]))),
			hi = 2 #FIXME
		)
		vx=vx*np.sign(rock.vel[0])
		output_vel = Math.Vector2([vx,vz])
		#Linear interpolation of velocity norm between PlatRock input vel and Toe's input one :
		out_vel_norm=rock.vel.norm()*output_vel.norm()/self.last_computed_data["input_vel"]
		if rolling: #if the rock was (azzoni-)rolling, also roll after contact
			rock.vel=Math.normalized2(rock.current_segment.branch)*out_vel_norm*np.sign(vx)
		else: #if the rock was flying, also do a fly after contact. NOTE: this is always the case for TwoDShape.
			output_vel=output_vel.normalized()*out_vel_norm
			rock.vel[0]=output_vel[0]
			rock.vel[1]=output_vel[1]
	
	def run_3D(self, rock, tree, xy_contact_point):
		vxy_rock=Math.Vector2(rock.vel[0:2])
		ecc_axis=Math.Vector2([-vxy_rock[1],vxy_rock[0]]).normalized() #the normed axis, orthogonal to vxy, on which the eccentricity is measured from the contact point and vxy
		ecc=(xy_contact_point-tree.pos).dot(ecc_axis)/(tree.dhp/2./100)	#eccentricity, from -1 to 1
		ang=np.sign(rock.vel[2])*abs(np.degrees(np.arctan(rock.vel[2]/vxy_rock.norm()))) # the vertical incident angle.
		angle=np.arctan2(vxy_rock[1],vxy_rock[0])	#the signed angle between the rock xy velocity and the +x axis. NOTE: arctan2:=arctan2(y,x)
		input_rock_vel_norm=rock.vel.norm()
		rock.vel[:] = self.get_output_vel(
			vel = rock.vel.norm(),
			vol = rock.volume,
			ecc = abs(ecc), # We use abs(ecc) as the DEM model is symetric, see the line below for ecc<0.
			dbh = tree.dhp,
			ang = ang,
			hi = 2 #FIXME
		) # The output vel here is expressed in Toe's C.S.
		if(ecc<0):rock.vel[1]*=-1
		rock.vel[0:2]=Math.rotated2(rock.vel[0:2],angle) #rotate the vel to translate from Toe's C.S to our global C.S.
		rock.vel=rock.vel.normalized()*input_rock_vel_norm*rock.vel.norm()/self.last_computed_data["input_vel"] #linear interpolation of velocity norm between PlatRock input vel and Toe's input one.
		
	
class Azzoni_Roll():
	"""
	Class capable of performing rocks roll on slopes, based on [Azzoni 1995]. The constructor will compute the stop distance (and optionally the stop position) on a supposed infinite slope. After that, you can retrieve the rock velocity at a given position with :meth:`get_vel`.
	
	Args:
		mass (float, optional): if :attr:`A` is not given, give the rock mass
		radius (float, optional): if :attr:`A` is not given, give the rock radius
		I (float, optional): if :attr:`A` is not given, give the rock inertia
	
	Attributes:
		vel (:class:`~Common.Math.Vector2`): the input rock velocity
		mu_r (float): the rolling friction, this is tan_roll_phi in Azzoni paper
		slope (float): the slope in radians
		gravity (float): the gravity
		start_pos (:class:`~Common.Math.Vector2`, optional): the rock input position, to compute the rock final position
		tan_slope (float, optional): stores the tangent of the slope, use in constructor only if you don't want the code to compute it from the slope
		A (float, optional): you can manually set this intermediate result, so you don't have to give the rock :attr:`mass`, :attr:`radius` and :attr:`I` (see [Azzoni 1995]).
		delta_tan_angles (float): the difference between the two tangents of angles (slope and mu).
		dist_stop (float): the resulting distance at which the rock will stop
		stop_pos (:class:`~Common.Math.Vector2`): the resulting position of the rock, if start_pos is given
		direction (int): stores the rock velocity direction along x: -1 or +1
		v_square (float): stores the square of the rock velocity norm
	"""
	
	def __init__(self,vel,mu_r,slope,gravity,start_pos=None,tan_slope=None,A=None,mass=None,radius=None,I=None):
		#INPUTS:
			#Mandatory:
		self.vel=vel
		self.mu_r=mu_r
		self.slope=slope
		self.gravity=gravity
			#Optional:
		self.start_pos=start_pos
		if tan_slope is None:
			self.tan_slope=np.tan(slope)
		else:
			self.tan_slope=tan_slope
		if A is None: #give either A or {mass,I,radius}
			self.A = mass/(mass+I/radius**2)
		else: self.A=A
		
		#OUTPUTS:
		self.delta_tan_angles=None
		self.dist_stop=None
		self.stop_pos=None #only if start_pos is given
		self.direction=None
		self.v_square=None
		
		#Depending on the rock environment, the variables below can be set by the simulation.
		#OTHER:
		self.until_stop=False
		
		self.compute_dist()
	
	def compute_dist(self):
		"""
		Computes the distance at which the rock will stop if it were on an infinite slope, and store it into :attr:`dist_stop`. If :attr:`start_pos` is set, also compute the :attr:`stop_pos`.
		
		Note:
			If the rock does an accelerated roll, :attr:`dist_stop` will be set to :math:`+\infty` and :attr:`stop_pos` will be set to [:math:`\pm\infty`, :math:`\pm\infty`]
		"""
		self.direction = -1 if self.vel[0]<0 else 1
		self.tan_slope*=self.direction #if going to -x direction, slope sign convention inverted
		self.delta_tan_angles = self.tan_slope - self.mu_r
		self.v_square=self.vel.norm()**2
		if(self.delta_tan_angles<0):#slow down rolling
			self.dist_stop=-self.v_square/(2*self.A*self.gravity*np.cos(self.slope)*self.delta_tan_angles)
			if(self.start_pos is not None):
				Dx=np.cos(self.slope)*self.dist_stop*self.direction
				Dy=-self.tan_slope*abs(Dx)
				self.stop_pos=self.start_pos+[Dx,Dy]
		else:
			self.dist_stop=np.inf
			self.stop_pos=Math.Vector2([self.direction*np.inf,self.direction*np.inf])
		
	def get_vel(self,arrival_point):
		"""
		Get the arrival velocity from an initiated instance of :class:`Azzoni_Roll` and an arrival point.
		
		Args:
			arrival_point (:class:`~Common.Math.Vector2`): the precomputed arrival point
		Returns:
			:class:`~Common.Math.Vector2`: the arrival velocity
		"""
		roll_dist=(arrival_point-self.start_pos).norm()
		scalar_vel = np.sqrt(2*self.A*self.gravity*np.cos(self.slope)*self.delta_tan_angles*roll_dist+self.v_square)
		return (arrival_point-self.start_pos).normalized()*scalar_vel
		


















