from platrock.Common.Simulations import GenericSimulation
from platrock.Common.Utils import ParametersDescriptorsSet, extract_geojson_to_params_set
from platrock.Common import Debug, ColorPalettes, Math, Outputs, ThreeDPostprocessings
import shapely, zipfile, os, copy
from osgeo import gdal
import numpy as np

import platrock

class GenericThreeDSimulation(GenericSimulation):
	valid_input_rocks_geojson_attrs=ParametersDescriptorsSet([
		[["number", "rocks_nb", "nb_rocks"],			"number",			"Rocks count",							int,	1,		1000000,	10],
		[["rocks_z", "z"],							"z",				"Drop height (m)\nAbove the terrain surface.",						float,	2,		50,		4],
		[["rocks_min_vol"],				"rocks_min_vol",	"Min rocks volume (m<sup>3</sup>)",		float,	1e-06,	100,		0.2],
		[["rocks_max_vol"],				"rocks_max_vol",	"Max rocks volume (m<sup>3</sup>)",		float,	1e-06,	100,		1],
		[["rocks_density", "density"],					"density",			"Rocks density (kg/m<sup>3</sup>)",		float,	100,	10000,	2650],
		[["rocks_vz", "vz"],						"vz",				"Vertical velocity (m/s)",				float,	-100,	100,		0]
	])
	
	# Useful in generic classes implementation :
	NB_SPACE_DIMS = 3
	SPACE_VECTOR_CLASS = Math.Vector3
	
	def __init__(self, rocks_start_params_geojson=None,checkpoints_geojson=None,**kwargs):
		super().__init__(**kwargs)
		self.iter=0
		self.checkpoints=[]
		self.rocks_start_params=[]
		self.current_start_params_id=0
		self.current_start_params_rock_id=0
		self.GUI_enabled=False
		if(rocks_start_params_geojson is not None):
			self.set_rocks_start_params_from_geojson(rocks_start_params_geojson)
		if(checkpoints_geojson is not None):
			self.set_checkpoints_from_geojson(checkpoints_geojson)
		self.limit_real_time_dt_interval=self.dt #used only with 3D view. Set equal to self.dt to compute real-time.
		self.last_time_computed=0
		self._geojson_polygon_offset_applied=False
		self.pp=None #this will be set to Postprocessings.Postprocessing(self) later
	
	def __init_arrays__(self):
		for start_zone in self.rocks_start_params:
			params=start_zone["params"]
			rocks_volumes = self.random_generator.rand(params["number"]) * ( params["rocks_max_vol"] - params["rocks_min_vol"] ) + params["rocks_min_vol"]
			params["rocks_volumes"]=rocks_volumes
	
	def set_rocks_start_params_from_geojson(self,rocks_start_params_geojson):
		self._geojson_polygon_offset_applied=False
		ret_message=extract_geojson_to_params_set(rocks_start_params_geojson,self.rocks_start_params,self.valid_input_rocks_geojson_attrs,ColorPalettes.dark2)
		self.__init_arrays__()
		return ret_message
	
	def set_checkpoints_from_geojson(self,checkpoints_geojson):
		try:
			self.checkpoints=[]
			shp_file=gdal.OpenEx(checkpoints_geojson)
			for feat in shp_file.GetLayer(0):
				feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
				points = np.asarray(feat_dict["geometry"]["coordinates"])
				if points.ndim == 3 : #sometimes the polyline is wrapped in an additional dimension (geojson)
					points=points[0]
				self.checkpoints.append(self.get_parent_module().Objects.Checkpoint(points))
			return 0
		except Exception as e:
			message="The importation of checkpoints from geojson failed:"+str(e)
			Debug.error(message)
			return message
	
	def save_to_file(self):
		"""
		Store (pickle to json) the simulation into a file whose path and name is the return result of :meth:`get_dir`. Note that the file will exclude all data that arises from calculations, this method is meant to save the simulation setup only.
		"""
		#store to local variables all data that shouldn't be saved to the file, then clear the corresponding simulation attributes :
		output=self.output
		self.output=None
		current_rock=self.current_rock
		self.current_rock=None
		pp=self.pp
		self.pp=None
		if(self.terrain):
			terrain=copy.copy(self.terrain)
			self.terrain.faces=np.array([])
			self.terrain.points=np.array([])
			self.terrain.trees=[]
			self.terrain.faces_xyz_bb=None
		checkpoints=self.checkpoints[:]
		self.checkpoints=[self.get_parent_module().Objects.Checkpoint(c.path) for c in checkpoints] #NOTE: keep the checkpoints position, drop the data
		if hasattr(self,'mechanicsHdf5Runner'):
				mechanicsHdf5Runner = self.mechanicsHdf5Runner
				self.mechanicsHdf5Runner=None
		if hasattr(self,"current_DS"):
			current_DS = self.current_DS
			self.current_DS = None
		if hasattr(self,"siconos_run_options"):
			siconos_run_options = self.siconos_run_options
			self.siconos_run_options = None
		super().save_to_file()	#actual file write is here
		#restore the not-saved data:
		self.output=output
		if(self.terrain):
			self.terrain=terrain
		self.checkpoints=checkpoints
		self.current_rock=current_rock
		self.pp=pp
		if hasattr(self,'mechanicsHdf5Runner'):
			self.mechanicsHdf5Runner=mechanicsHdf5Runner
		if hasattr(self,"current_DS"):
			self.current_DS = current_DS
		if hasattr(self,"siconos_run_options"):
			self.siconos_run_options = siconos_run_options
		Debug.info("... DONE")
	
	def results_to_zipfile(self,filename=None):
		"""
		Create a zip file into the folder returned by :meth:`get_dir` named results.zip containing two text files. "stops.csv" contains info about rocks end position, and "checkpoints.csv" contains the checkpoints infos.
		"""
		self.output.write_to_h5(self.get_dir()+'full_output.hdf5')
		if(filename is None):
			filename=self.get_dir()+"results.zip"
		zf = zipfile.ZipFile(filename, "w")
		zf.write(self.get_dir()+'full_output.hdf5', 'full_output.hdf5')
		if not self.pp.has_run:
			self.pp.run()
		outputs=self.pp.raster.output_to_asc(output_to_string=True)
		for field,output in outputs.items():
			zf.writestr(field+".asc",output)

		if(os.path.isfile(self.get_dir()+"terrain_overview.pdf")):
			zf.write(self.get_dir()+"terrain_overview.pdf",arcname="trajectories_overview.pdf")
		
		output_str="checkpoint_id;vx;vy;vz;volume;x;y;z;angVelx;angVely;angVelz;Ec_t;Ec_r\n"
		for chckpt_id,chckpt in enumerate(self.checkpoints):
			for i in range(len(chckpt.rocks_ids)):
				rock_id=chckpt.rocks_ids[i]
				mass=self.output.volumes[rock_id]*self.output.densities[rock_id]
				output_str+=str(chckpt_id)+";"
				output_str+=str(chckpt.vels[i][0])+";"
				output_str+=str(chckpt.vels[i][1])+";"
				output_str+=str(chckpt.vels[i][2])+";"
				output_str+=str(self.output.volumes[rock_id])+";"
				output_str+=str(chckpt.pos[i][0])+";"
				output_str+=str(chckpt.pos[i][1])+";"
				output_str+=str(chckpt.pos[i][2])+";"
				output_str+=str(chckpt.angVels[i][0])+";"
				output_str+=str(chckpt.angVels[i][1])+";"
				output_str+=str(chckpt.angVels[i][2])+";"
				output_str+=str(0.5*mass*Math.Vector3(chckpt.vels[i]).norm()**2)+";"
				output_str+=str(0.5*np.dot(chckpt.angVels[i],np.dot(self.output.inertias[rock_id],chckpt.angVels[i])))+"\n"
		zf.writestr("checkpoints.csv",output_str)

		zf.close()
	
	def update_checkpoints(self):
		"""
		Update all the simulation :class:`ThreeD.Objects.Checkpoint` according to all contacts of all rocks. This is a post-processing feature, it is supposed to be triggered after the simulation end.
		"""
		for chkP in self.checkpoints:
			chkP.init_data(self)
		for ri in range(self.nb_rocks):
			contacts_pos=self.output.get_contacts_pos(ri)
			contacts_shapely_linestring=shapely.geometry.LineString(contacts_pos[:,:2]) #2D rock trajectory as a shapely linestring.
			#The following terrific 2 lines converts the rock contact points into the 2D distance traveled by the rock at each contact (so its a 1D array starting with value 0). See below for usage.
			dist_travelled_at_contacts=np.roll(np.cumsum(np.sqrt(((contacts_pos[:,:2]-np.roll(contacts_pos[:,:2],-1,axis=0))**2).sum(axis=1))),1,axis=0)
			dist_travelled_at_contacts[0]=0
			for chkP in self.checkpoints:
				#Shapely is very performant at finding the intersection between two polylines (=linestring)
				if contacts_shapely_linestring.intersects(chkP.shapely_linestring): 
					i=contacts_shapely_linestring.intersection(chkP.shapely_linestring)
					if type(i).__name__ == 'GeometryCollection': continue
					if type(i).__name__ == 'MultiPoint' and len(i.geoms)>0:
						i=i.geoms[0]
					if type(i).__name__ == 'Point':
						#But shapely can't directly give us the contact (=polyline point) just before the intersection.
						#That's why we use our `dist_travelled_at_contacts` array in combination with shapely's `project` function to find it out.
						dist=contacts_shapely_linestring.project(i)
						id_before=np.where(dist_travelled_at_contacts<dist)[0][-1]
						prev_pos=contacts_pos[id_before]
						prev_vel=self.output.get_contacts_vels(ri)[id_before]
						if abs(prev_vel[0])>abs(prev_vel[1]) :
							flight_time=(i.x-prev_pos[0])/prev_vel[0]
						else:
							flight_time=(i.y-prev_pos[1])/prev_vel[1]
						absolute_height=-0.5*self.gravity*flight_time**2 + prev_vel[2]*flight_time + prev_pos[2]
						vel=Math.Vector3([prev_vel[0], prev_vel[1], prev_vel[2] - self.gravity*flight_time])
						chkP.rocks_ids.append(ri)
						chkP.pos.append(i.coords[0]+(absolute_height,))
						chkP.vels.append(vel)
						chkP.angVels.append(self.output.get_contacts_angVels(ri)[id_before]) #assume constant in flight
		for chkP in self.checkpoints:
			chkP.crossings_ratio=len(chkP.rocks_ids)/self.nb_rocks
		self.output.checkpoints=self.checkpoints
	
	def before_run_tasks(self):
		if self.GUI_enabled :
			self.status="pause"
		else:
			self.status="running"
		#Initialize overall nb_rocks from the sum of start zones:
		self.nb_rocks=0
		for params_zone in self.rocks_start_params:
			self.nb_rocks+=params_zone["params"]["number"]
		#Offset the position of the start params polygons:
		if not self._geojson_polygon_offset_applied:
			for rsp in self.rocks_start_params:
				rsp["shapely_polygon"] = shapely.affinity.translate(rsp["shapely_polygon"],xoff=-self.terrain.Z_raster.xllcorner,yoff=-self.terrain.Z_raster.yllcorner)
			self._geojson_polygon_offset_applied=True
		#Offset the soil params polygons:
		if not self.terrain._geojson_polygon_soil_offset_applied:
			for sp in self.terrain.soil_params:
				sp["shapely_polygon"] = shapely.affinity.translate(sp["shapely_polygon"],xoff=-self.terrain.Z_raster.xllcorner,yoff=-self.terrain.Z_raster.yllcorner)
			self.terrain._geojson_polygon_soil_offset_applied=True
		#Offset the forest params polygons:
		if not self.terrain._forest_offset_applied:
			for sp in self.terrain.forest_params:
				sp["shapely_polygon"] = shapely.affinity.translate(sp["shapely_polygon"],xoff=-self.terrain.Z_raster.xllcorner,yoff=-self.terrain.Z_raster.yllcorner)
			if "trees_array" in self.terrain.automatic_generate_forest.keys(): #case of xyd input
				trees_array=self.terrain.automatic_generate_forest["trees_array"]
				trees_array[:,0]-=self.terrain.Z_raster.xllcorner
				trees_array[:,1]-=self.terrain.Z_raster.yllcorner
			self.terrain._forest_offset_applied=True

		#call the parent function, which needs nb_rocks to be initialized:
		super().before_run_tasks()
		
		self.current_start_params_rock_id=0
		self.current_start_params_id=0
		
		if(platrock.web_ui):
			self.terrain.populate_from_Z_raster()
			self.terrain.precompute_datas()
			self.terrain.automatic_generate_forest["enable"]=True
			self.__init_arrays__()

		self.terrain.set_faces_params_from_geojson()
		
		if(self.terrain.automatic_generate_forest["enable"]):
			self.terrain.generate_forest()
			self.enable_forest=len(self.terrain.trees)>0
		if self.enable_forest:
			self.terrain.trees_as_array=np.asarray([np.append(t.pos,t.dhp) for t in self.terrain.trees])
		
		if platrock.web_ui:
			ThreeDPostprocessings.ThreeDPostprocessing(self) #this will set self.pp
			self.pp.run_init()
	
	def pick_rock_start_xy(self):
		params=self.rocks_start_params[self.current_start_params_id]['params']
		polygon=self.rocks_start_params[self.current_start_params_id]['shapely_polygon']
		if(isinstance(polygon,shapely.geometry.MultiPolygon)):
			rand=self.random_generator.rand()
			ID=np.where(self.rocks_start_params[self.current_start_params_id]["multipoly_normalized_area_cumsum"]>rand)[0][0]
			polygon=polygon.geoms[ID]

		#find a rock start x,y pos in the polygon:
		min_x, min_y, max_x, max_y = polygon.bounds
		for i in range(1000):
			random_point = shapely.geometry.Point([self.random_generator.uniform(min_x, max_x), self.random_generator.uniform(min_y, max_y)])
			if(polygon.contains(random_point)):
				return (random_point.x,random_point.y)
		Debug.error("Unable to generate a point in the given polygon after 1000 tries.")


	def before_rock_launch_tasks(self):
		#select the right parameter set from self.rocks_start_params by using the sub-counter self.current_start_params_rock_id
		params=self.rocks_start_params[self.current_start_params_id]['params']
		self.current_start_params_rock_id+=1
		if(self.current_start_params_rock_id>params["number"]):
			self.current_start_params_id+=1
			self.current_start_params_rock_id=1
		self.iter=0
		
		self.add_rock()
		self.setup_rock_kinematics()
		
		# Reset forest:
		if(self.terrain):
			for tree in self.terrain.trees:
				tree.active=True
				tree.color=[0,0.8,0]
		super().before_rock_launch_tasks()
	
	def after_rock_propagation_tasks(self,*args,**kwargs):
		super().after_rock_propagation_tasks(*args,**kwargs)
		if(self.current_rock.out_of_bounds):
			self.output.add_contact(self.current_rock,Math.Vector3([0.,0.,0.]),Outputs.OUT)
		else:
			self.output.add_contact(self.current_rock,Math.Vector3([0.,0.,0.]),Outputs.STOP)
		if platrock.web_ui:
			self.pp.run_one_rock()
	
	def after_successful_run_tasks(self,*args,**kwargs):
		super().after_successful_run_tasks(*args,**kwargs)
		self.update_checkpoints()
		if platrock.web_ui:
			# ThreeDPostprocessings.ThreeDPostprocessing(self) #this will set self.pp
			# self.pp.run()
			self.pp.run_end()
			import platrock.GUI.Plot3D as Plot3D
			with open(self.get_dir()+'terrain_overview_plotly.html','w') as f:
				f.write(Plot3D.get_plotly_raw_html(self,100))
			self.results_to_zipfile()
	
	def after_all_tasks(self,*args,**kwargs):
		super().after_all_tasks(*args,**kwargs)
	
	def run(self,GUI=False, **kwargs):
		if(GUI and self.GUI_enabled==False):	#ThreeD GUI only
			self.GUI_enabled=True
			import platrock.GUI.View3D
			platrock.GUI.View3D.initialize(self)
		else:
			super().run(**kwargs)
	def get_forest_params_verification_report(self, report=None):
		if report is None :
			report = Report()
		if len(self.terrain.forest_params)>0:
				report.add_info("Forest is activated.")
				for i,param_set in enumerate(self.terrain.forest_params):
					if not 'shapely_polygon' in param_set.keys():
						report.add_error( "No polygon found in forest parameter set #%s."%(i) )
					else:
						polygon=param_set["shapely_polygon"]
						if not (isinstance(polygon,shapely.geometry.MultiPolygon) or isinstance(polygon,shapely.geometry.Polygon)):
							report.add_error( "The polygon is invalid in forest parameter set #%s."%(i) )
					params_descriptors=self.forest_impact_model.valid_input_attrs
					for param_desc in params_descriptors.parameters:
						if param_desc.inst_name not in param_set['params'].keys():
							report.add_error( "The parameter name %s is missing in forest parameters set #%s"%(param_desc.inst_name,i) )
						else:
							param_value=param_set['params'][param_desc.inst_name]
							report.check_parameter(param_desc,param_value,location_string="forest parameters set #%s"%(i))
		else:
			report.add_info("Forest is disabled.")
		return report
