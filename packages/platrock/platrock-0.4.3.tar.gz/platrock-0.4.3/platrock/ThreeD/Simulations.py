"""
"""

"""
This module is used by the ThreeD model. It is a kind of master module that handles simulations.
"""

from . import Objects, Engines
from platrock.Common.ThreeDObjects import Point
from platrock.Common import Debug, BounceModels, Math
from platrock.Common.ThreeDSimulations import GenericThreeDSimulation
from platrock.Common.TimeSteppedSimulations import GenericTimeSteppedSimulation
from platrock.Common.Utils import Report
import numpy as np
import quaternion, time, sys
import osgeo.gdal as gdal
if(int(gdal.__version__.split('.')[0])<2):
	Debug.error("python3-gdal version is ",gdal.__version__,"but must be >=2. If you are using ubuntu 16.04 or earlier, you may consider using 'sudo add-apt-repository -y ppa:ubuntugis/ppa'.")
	sys.exit()
import shapely.geometry
import shapely.affinity
from matplotlib import cm

class Simulation(GenericThreeDSimulation, GenericTimeSteppedSimulation):
	"""
	A simulation
	
	.. _input_threeD_params:
	
	The table below displays the attributes that have to be set to the polygons of the input geojson rocks_start_params_geojson depending on the sub-model choosen.
	
	+------------------+--------------+---------+--------------+-----------+--------------+-------------+--------------+
	|                  |:attr:`number`|:attr:`z`|:attr:`volume`| :attr:`vz`|:attr:`length`|:attr:`width`|:attr:`height`|
	+------------------+--------------+---------+--------------+-----------+--------------+-------------+--------------+
	|PlatRock (builtin)|            * |       * |     *        |     *     |              |             |              |
	+------------------+--------------+---------+--------------+-----------+--------------+-------------+--------------+
	|Siconos           |            * |   *     |              |     *     |       *      |       *     |       *      |
	+------------------+--------------+---------+--------------+-----------+--------------+-------------+--------------+

	
	Args:
		rocks (list [:class:`ThreeD.Objects.Rock`]): list of all rocks, created in the launching script (see Examples/3D.py)
		current_rock (:class:`ThreeD.Objects.Rock`): the rock currently falling
		terrain (:class:`ThreeD.Objects.Terrain`): the terrain of the simulation
		gravity (float): the --- positive --- gravity acceleration value
		enable_forest (bool): whether to take trees into account or not
		engines (list [:class:`ThreeD.Engines.Engine`]): list of engines to run at each timestep
		dt (int): the time-step
		iter (int): the current iteration (reseted at each new rock)
		running (bool): whether the simulation is running
		enable_GUI (bool): enables the 3D view (experimental)
	"""
	webui_typename="PlatRock 3D"
	valid_input_rocks_geojson_attrs=GenericThreeDSimulation.valid_input_rocks_geojson_attrs
	
	def __init__(self, engines=None, dt=0.02, **kwargs):
		GenericTimeSteppedSimulation.__init__(self, dt = dt)
		super().__init__(**kwargs)
		self.engines=engines or [
			Engines.Verlet_update(use_cython=True,dist_factor=5),
			Engines.Contacts_detector(use_cython=True),
			Engines.Rock_terrain_nscd_basic_contact(),
			Engines.Rock_tree_nscd_basic_contact(),
			Engines.Nscd_integrator(use_cython=True)
		]
	
	def add_rock(self):
		params=self.rocks_start_params[self.current_start_params_id]['params']
		self.current_rock=Objects.Sphere(
			volume=params["rocks_volumes"][self.current_start_params_rock_id-1], #NOTE: current_start_params_rock_id starts at 1
			density=params["density"]
		)
	
	def setup_rock_kinematics(self):
		params=self.rocks_start_params[self.current_start_params_id]['params']
		# Pick a start point x y
		start_point = Point(*self.pick_rock_start_xy(), np.nan)

		#FIXME: take the spherical shape of the rock into account.
		#find the face below the rock then set the rock altitude:
			#1- use the faces bounding boxes in the (x,y) plane to get a rough list
		mins_check_outside = (start_point.pos[0:2]<self.terrain.faces_xyz_bb[:,0:3:2]).any(axis=1)
		maxs_check_outside = (start_point.pos[0:2]>self.terrain.faces_xyz_bb[:,1:5:2]).any(axis=1)
		inside_mask = np.logical_not(np.logical_or(mins_check_outside, maxs_check_outside))
			#2- loop on the faces list to get the face right below the rock
		for f in self.terrain.faces[inside_mask]:
			#find the corresponding face:
			if(f.is_point_inside_2D(start_point)):	#find the Z position of the rock right above the corresponding face
				start_point.pos[2] = -(f.normal[0]*(start_point.pos[0]-f.points[0].pos[0]) + f.normal[1]*(start_point.pos[1]-f.points[0].pos[1]))/f.normal[2]+f.points[0].pos[2]+params["z"]+self.current_rock.radius
				break

		vel=Math.Vector3([self.random_generator.rand()*0.01,self.random_generator.rand()*0.01,params["vz"]])
		self.current_rock.setup_kinematics(
			pos = start_point.pos,
			vel = vel,
			angVel = [0, 0, 0],
			ori= [0, 0, 0]
		)

		if np.isnan(start_point.pos[2]):
			Debug.error("Couldn't find a face right below the current rock center, so the height couldn't be set. [X,Y] coords were", start_point.pos[:2])
			self.current_rock.is_stopped = True
			self.current_rock.pos[2] = 0

	def rock_propagation_tasks(self):
		#Don't call the parent function here as it would be useless as there is nothing in the parent class (nothing common between TwoD and ThreeD)
		if(not self.status=="running"):
			time.sleep(0.1)
			return
		if(self.GUI_enabled):
			if time.time()-self.last_time_computed < self.limit_real_time_dt_interval:
				return
			self.last_time_computed=time.time()
			for f in self.current_rock.verlet_faces_list:
				f.color=[0.68235294, 0.5372549 , 0.39215686]
		for E in self.engines:
			if( (not E.dead) and self.iter%E.iter_every==0):E.run(self)
		if(self.GUI_enabled):
			for f in self.current_rock.verlet_faces_list:
				f.color=[0.82352941, 0.41176471, 0.11764706]
			if(self.current_rock.terrain_active_contact):
				self.current_rock.terrain_active_contact.face.color=np.random.rand(3)
		if(self.vel_stop_condition()):
			self.current_rock.is_stopped=True
			Debug.info("Rock stopped")
			if(self.GUI_enabled):
				for f in self.current_rock.verlet_faces_list:
					f.color=[0.68235294, 0.5372549 , 0.39215686]
		self.iter+=1
	
	def get_parameters_verification_report(self):
		report = Report()
		
		#HAS TERRAIN:
		if self.terrain is None:
			report.add_error("The simulation has no terrain.")
		
		#REBOUND PARAMETERS CHECK:
		if self.override_rebound_params:
			report.add_error( "self.override_rebound_params==True is not yet supported in WebUI." )
		
		for i,param_set in enumerate(self.terrain.soil_params):
			if not 'shapely_polygon' in param_set.keys():
				report.add_error( "No polygon found in soil parameter set #%s."%(i) )
			else:
				polygon=param_set["shapely_polygon"]
				if not (isinstance(polygon,shapely.geometry.MultiPolygon) or isinstance(polygon,shapely.geometry.Polygon)):
					report.add_error( "The polygon is invalid in soil parameter set #%s."%(i) )
			if (("bounce_model_number" not in param_set['params'].keys()) or 
				(param_set['params']['bounce_model_number'] not in BounceModels.number_to_model_correspondance.keys())):
				report.add_error( "The bounce_model_number is missing or invalid in soil parameters set #%s"%(i) )
			else:
				params_descriptors=BounceModels.number_to_model_correspondance[param_set['params']['bounce_model_number']].valid_input_attrs
			for param_desc in params_descriptors.parameters:
				if param_desc.inst_name not in param_set['params'].keys():
					report.add_error( "The parameter name %s is missing in soil parameters set #%s"%(param_desc.inst_name,i) )
				else:
					param_value=param_set['params'][param_desc.inst_name]
					report.check_parameter(param_desc,param_value,location_string="soil parameters set #%s"%(i))
			
		report = self.get_forest_params_verification_report(report)
		return report















