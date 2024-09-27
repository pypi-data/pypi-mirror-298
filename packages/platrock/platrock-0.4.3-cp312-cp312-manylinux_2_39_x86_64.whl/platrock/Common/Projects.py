"""
"""

"""
Definition of the project class
"""

from . import Debug
import os, re, glob, fnmatch, traceback, jsonpickle, fasteners
import numpy as np
import platrock.ThreeD.Simulations
from platrock.Common.Simulations import GenericSimulation
from platrock.Common.TwoDObjects import GenericTwoDTerrain
from . import RetroCompatibility
projects_root=""
projects_list=[]

class Project(object):
	def __init__(self):
		self.name=""
		self.date=""
		self.author=""
		self.location=""
		self.context=""
		self.aims=""
		self.path=""
		self.simulations=[]
	
	def write_to_file(self):
		path=self.path+"/PlatRockProject"
		f=open(path,'w',encoding="utf8")
		for k in self.__dict__:
			if k in ["path","simulations_names"]:continue
			f.write('###'+k+'\n')
			f.write(str(self.__dict__[k])+"\n")
		f.close()
	
	def get_loaded_simulation(self,path):
		# If a worker thread is currently writing into the setup.json file, then the file content will be equal to "".
		# For that case, use a process lock mechanism.
		Debug.info('Loading simulation located at',path)
		r=None
		with GenericSimulation.get_setup_lock_from_path(path):
			with open( path, "r",encoding="utf8") as f:
				r=f.read()
		try:
			s=RetroCompatibility.decode_legacy_json(r)
			if type(s)==dict :
				Debug.warning("Jsonpickle didn't found a corresponding class for",path)
				return s
			if isinstance(s.terrain,GenericTwoDTerrain) : #we didn't save the param_zones as jsonpickle don't handle weird types, reconstruct here.
				s.terrain.set_params_zones()
		except Exception:
			Debug.error("Jsonpickle was unable to load the simulation",path,". The error was:",traceback.format_exc())
			s=None
		return s
	
	def update_simulations_list(self):
		simulations=[]
		sim_dirs=next(os.walk(self.path))[1]
		sim_dirs.sort()
		for sim_dir in sim_dirs:
			sim_dir=self.path+"/"+sim_dir
			sim_file=glob.glob(sim_dir+'/setup.json')
			if(len(sim_file)>0):
				s=self.get_loaded_simulation(sim_file[0])
				if type(s)==dict : continue
				elif(s==None): #the file was not readable for some reason
					Debug.warning("The file",sim_file[0],"could not be opened.")
					for s2 in self.simulations: #search in the existing simulations list in memory
						if(s2.get_full_path()==sim_file[0]):
							s=s2	#if found, keep the one in memory instead of loading
							break
					#If we are here, the file couldn't be loaded and the simulation is not present in memory.
					continue
				s.project=self
				simulations.append(s)
		self.simulations=simulations
		
	def reload_simulation(self,simulation):
		s=self.get_loaded_simulation(simulation.get_full_path())
		if(s):
			s.project=self
			for i in range(len(self.simulations)):
				if(self.simulations[i].get_full_path()==s.get_full_path()):
					self.simulations[i]=s
					break
			return s
		else:
			return simulation
	
	def has_simulation_name(self,name):
		if name in [s.name for s in self.simulations]:
			return True
		else:
			return False
	
	def find_simulation_by_name(self,name):
		for s in self.simulations:
			if s.name==name:
				return s
		return None

def find_by_name(name):
	for p in projects_list:
		if(p.name==name):
			return p

def exists(name):
	if name in [p.name for p in projects_list]:
		return True
	else:
		return False

def update_projects_list():
	global projects_list
	projects_list=[]
	w=os.walk(projects_root)
	for path, dirs, files in w:
		for filename in files:
			if(filename=="PlatRockProject"):
				f=open(path+"/"+filename,'r',encoding="utf8")
				filestring=f.read()
				f.close()
				filestring=re.sub(' *\\n','\\n',filestring)
				p=Project()
				p.path=path
				for argname in ["name","date","author","location","context","aims"]:
					if("###"+argname) in filestring:
						value=filestring.split("###"+argname+"\n")[1].split("\n###")[0]
						value=value.strip()
						p.__dict__[argname]=value
				projects_list.append(p)
