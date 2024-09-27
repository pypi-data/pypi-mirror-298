"""
A placeholder for Simulation in the Common module. This module gather all simulations common things for TwoD, ThreeD, TwoDShape, models (and maybe others added afterwards).
"""


import time,traceback,yappi,psutil,multiprocessing
import numpy as np
import subprocess,os,sys
from . import BounceModels
import platrock.Common.Debug as Debug
from platrock.Common import Outputs
import time, os, sys, traceback, jsonpickle, fasteners
import jsonpickle.ext.numpy as jsonpickle_numpy
jsonpickle_numpy.register_handlers()
jsonpickle.set_encoder_options('simplejson', indent=1)

import platrock

class GenericSimulation(object):
	"""
	Generic :class:`Simulation`, parent of all simulations from PlatRock main modules (TwoD, ThreeD, TwoDShape, ...). It contains common attributes and functions. A :class:`Simulation` object contains all informations concerning PlatRock simulations. Its child type defines the simulation model, its attributes stores the simulation setup and outputs. The run() method is used to launch the simulation (loops on rocks) via a set of generic methods.
	
	Args:
		random_seed (int, optional): if given the random generator will be sed with this value, making simulation reproductible.

	Attributes:
		name (string): the simulation name, useful for GUIs
		terrain (compatible :class:`Terrain`): binds a terrain to this simulation, must be compatible with the :class:`Simulation` type.
		gravity (float): positive gravity value
		project (:class:`Common.Projects.Project`): the project that contains this simulation, useful for GUIs
		enable_forest (bool): whether to enable the forest or not
		status (string): reflects the simulation state, will be modified internally
		use_retro_compatibility (bool): whether this simulation was loaded by :py:mod:`RetroCompatibility` or not
		forest_impact_model (:class:`Common.BounceModels` subclass): a bounce model that will handle rock-tree contacts, defaults to :class:`Common.BounceModels.Toe_Tree`
		nb_rocks (int): how many rocks to launch, will be set internally
		current_rock (compatible :class:`Rock`): points to the current simulated rock, will be set internally
		benchmark (bool): whether to enable yappi profiling tool or not
		checkpoints (list of compatible :class:`Checkpoint`): the list of compatible checkpoints, will be set internally
		output (:class:`Common.Outputs.Output`): binds to the output instance, useful to retrieve simulation results
		current_rock_number (int): how many rocks have already propagated, will be set internally
		random_generator (:class:`numpy.random.RandomState`): set internally
		override_forest_params (bool): whether to globally override all forest parameters or not
		override_rebound_params (bool): whether to globally override all soil parameters or not
		override_[param_name] (various): where [param_name] are the soil/forest parameter to override (ex: override_R_n)
	"""

	@staticmethod
	def get_setup_lock_from_path(setup_path):
		lock_filename = setup_path.rsplit("/",1)[0]+"/setup.json.lock"
		return fasteners.InterProcessLock(lock_filename)
	
	@classmethod
	def get_parent_module(cls):
		for ancestor in cls.__mro__:
			if 'platrock.' in ancestor.__module__:
				return sys.modules[ancestor.__module__]
		raise TypeError("Couldn't find the simulation parent module. Did you make an exotic platrock import or subclassing ?")

	def __init__(self, terrain=None, gravity=9.8, name=None, project=None, enable_forest=False, random_seed=None):
		t=time.localtime()
		if(name==None):self.name="New simulation ("+str(t.tm_mday).rjust(2,'0')+"-"+str(t.tm_mon).rjust(2,'0')+"-"+str(t.tm_year)+", "+str(t.tm_hour).rjust(2,'0')+":"+str(t.tm_min).rjust(2,'0')+":"+str(t.tm_sec).rjust(2,'0')+")"
		else:self.name=str(name)
		self.terrain=terrain
		self.gravity=gravity
		self.project=project
		self.enable_forest=enable_forest
		self.status="init"
		self.use_retro_compatibility=False
		self.forest_impact_model=None
		self.nb_rocks=0
		self.current_rock=None
		self.benchmark=False
		self.checkpoints=None
		self.output=None
		self.current_rock_number=-1
		self.stop_vel_threshold = 0.2
		
		#OVERRIDE PARAMETERS :
		self.override_forest_params=False
		self.override_rebound_params=False
		self.number_to_bounce_model_instance = {}
		
		if(random_seed==None):
			self.random_generator=np.random.RandomState()
		else:
			self.random_generator=np.random.RandomState(random_seed)
		
		#initialize the tree impact model here for every simulation, as it is needed in get_parameters_verification_report
		self.forest_impact_model=BounceModels.Toe_Tree_2022()

		self.additional_data_to_queue = {}

	def get_terrain_cls(self):
		return self.get_parent_module().Objects.Terrain
	
	def get_full_path(self):
		"""
		Get the full path of the simulation pickle file, composed of: "/the_project_path/simulation_name/setup.json"
		
		Returns:
			string
		"""
		if(self.project):
			return self.project.path+"/"+self.name+"/setup.json"
		else:
			Debug.info("This simulation has no project.")
			return "./"+self.name+"/setup.json"
	
	def get_dir(self):
		"""
		Get the path corresponding to the simulation, its the basepath of setup.json.
		
		Returns:
			string
		"""
		return self.get_full_path().rsplit("/",1)[0]+"/"
	
	def get_setup_lock(self):
		return self.get_setup_lock_from_path(self.get_full_path())
	
	def save_to_file(self):
		"""
		This method will write the simulation into a json file located at :meth:`get_full_path` with jsonpickle.
		
		Note:
			This method is not intented to be used as it, rather call it from the simulation subclass as we must before remove the unwanted heavy attributes.
		"""
		Debug.info("Save simulation...")
		prefix=self.get_dir()
		if(not os.path.isdir(prefix)):
			subprocess.call(["mkdir",prefix])
		
		#CLEANUPS
		if hasattr(self,'forest_impact_model') and hasattr(self.forest_impact_model,'toe_array'):
			toe_array = self.forest_impact_model.toe_array
			self.forest_impact_model.last_computed_data={}
			self.forest_impact_model.toe_array = None
		if hasattr(self,'number_to_bounce_model_instance'):
			number_to_bounce_model_instance=self.number_to_bounce_model_instance
			self.number_to_bounce_model_instance={}

		#ACTUAL WRITES
		with self.get_setup_lock():
			with open(self.get_full_path(), "w", encoding="utf8") as f:
				#One more cleanup, placed here because get_setup_lock and get_full_path needs self.project to be set.
				project=self.project
				self.project=None
				f.write(jsonpickle.encode(self,keys=True))
		
		#RESTORES
		self.project=project
		if hasattr(self,'forest_impact_model') and hasattr(self.forest_impact_model,'toe_array'):
			self.forest_impact_model.toe_array = toe_array
		if hasattr(self,'number_to_bounce_model_instance'):
			self.number_to_bounce_model_instance=number_to_bounce_model_instance
	
	def vel_stop_condition(self):
		if len(self.output.contacts[-1])>=2 and self.current_rock.vel.norm()<self.stop_vel_threshold :
			Debug.info('STOP CONDITION with current vel = '+str(self.current_rock.vel))
			return True
		return False
	
	def abort(self):
		"""
		If this simulation is launched via a GUI, this will abord its subprocess according to the process name, which sould be set to :meth:`get_full_path`.
		"""
		for p in multiprocessing.active_children():
			if p.name == self.get_full_path():
				psut=psutil.Process(p.pid)
				for child_process in psut.children() :
					child_process.send_signal(psutil.signal.SIGKILL)
				p.terminate()
		try:
			self.after_failed_run_tasks()
			self.save_to_file()
		except Exception:
			pass
	
	def before_run_tasks(self):
		"""
		Task method called right after a simulation is launched.
		"""
		Debug.add_logger(self.get_dir()+"log.txt")
		self.current_rock_number=-1
		self.output=Outputs.Output(self)
		if(self.benchmark):
			yappi.set_clock_type("wall")
			yappi.clear_stats()
			yappi.start(builtins=True)
		#initialize the bounce models NOTE: must be placed after the random_generator:
		for number in BounceModels.number_to_model_correspondance.keys():
			self.number_to_bounce_model_instance[number]=BounceModels.number_to_model_correspondance[number](self) # instanciation of each model
		#Remove the eventual results zipfile already created:
		filename=self.get_dir()+"results.zip"
		if os.path.exists(filename):
			os.remove(filename)

	def before_rock_launch_tasks(self):
		print("Rock nb", self.current_rock_number)
		print("Rand seed", self.current_rock_number+340)
		self.random_generator=np.random.RandomState(self.current_rock_number+340)
		np.random.seed(0)
		"""
		Task method called before each rock propagation.
		"""
		Debug.info("\n-----------------------------------\n.....::::: NEW ROCK N"+str(self.current_rock_number)+" at pos "+str(self.current_rock.pos)+" and vel "+str(self.current_rock.vel)+":::::.....\n-----------------------------------\n")
		self.output.add_rock(self.current_rock)
		self.output.add_contact(  #store the rock initial position
			self.current_rock,
			0*self.current_rock.pos,
			Outputs.START
		)
	
	def rock_propagation_tasks(self):
		"""
		Here is the science, this task method must do the propagation main loops for a single rock.
		"""
		return
	
	def after_rock_propagation_tasks(self,queue=None):
		"""
		Task method called after each single rock propagation is finished.
		
		Args:
			queue (:class:`multiprocessing.Queue`, optional): if given, communicates a dict with :attr:`status`, :attr:`rocks_done`, :attr:`nb_rocks` after each rock propagation.
		"""
		if queue:
			send_dict = {"status":self.status,"rocks_done":self.current_rock_number+1,"nb_rocks":self.nb_rocks}
			send_dict.update(self.additional_data_to_queue)
			queue.put_nowait(send_dict)
			self.additional_data_to_queue={}
	
	def after_successful_run_tasks(self):
		"""
		Task method called after all the rocks are propagated, if everything went right.
		"""
		self.status="finished"
	
	def after_failed_run_tasks(self):
		"""
		Task method called if an error occurs.
		"""
		self.status="error"
		Debug.error(traceback.format_exc())
		
	def after_all_tasks(self,queue=None):
		"""
		Task method called after all rocks propagations are finished.
		
		Args:
			queue (:class:`multiprocessing.Queue`, optional): if given, communicates a dict with :attr:`status`, :attr:`rocks_done`, :attr:`nb_rocks`.
		"""
		if queue:
			send_dict = {"status":self.status,"rocks_done":self.current_rock_number+1,"nb_rocks":self.nb_rocks}
			send_dict.update(self.additional_data_to_queue)
			queue.put_nowait(send_dict)
			self.additional_data_to_queue={}
		if(self.benchmark):
			yappi.stop()
			fs=yappi.get_func_stats()
			fs.sort('ttot')
			fs.print_all( columns={0: ('name', 100), 1: ('ncall', 8), 2: ('ttot', 8), 3: ('tsub', 8), 4: ('tavg', 8)} )
		if platrock.web_ui:
			self.save_to_file()
			Debug.info("Simulation located in "+self.get_full_path()+" finished with status "+self.status+".")
		else:
			Debug.info("Simulation finished with status "+self.status+".")
	
	def run(self,GUI=False,queue=None):
		"""
		Actually launch the simulation, contains the main loop on rocks and the calls to all other task methods.
		
		Args:
			GUI (bool): enables the ThreeD 3D view
			queue (:class:`multiprocessing.Queue`, optional): this queue will be passed to other methods to communicate.
		"""
		try:
			self.before_run_tasks()
		except:
			self.after_failed_run_tasks()
			self.after_all_tasks(queue=queue)
			return
		try:
			while self.current_rock_number<self.nb_rocks-1 :
				self.current_rock_number+=1
				self.before_rock_launch_tasks()
				while( not self.current_rock.is_stopped):
					self.rock_propagation_tasks()
				self.after_rock_propagation_tasks(queue=queue)
			self.after_successful_run_tasks()
		except KeyboardInterrupt:
			pass
		except Exception:
			self.after_failed_run_tasks()
		finally:
			self.after_all_tasks(queue=queue)

