"""
Some handy classes and functions used everywhere in PlatRock.
FIXME: DOC
"""

from osgeo import gdal
import functools,operator,copy
import numpy as np
from . import Debug, PyUtils
import shapely.geometry

def parameterDescriptorFactory(*args, **kwargs):
	if args[0]=='FreeNumber':
		return FreeNumberParameterDescriptor(*args[1:], **kwargs)
	elif args[0]=='StringChoice':
		return StringChoiceParameterDescriptor(*args[1:], **kwargs)
	elif args[0]=='FreeString':
		return FreeStringParameterDescriptor(*args[1:], **kwargs)
	elif args[0]=='Bool':
		return BoolParameterDescriptor(*args[1:], **kwargs)
	elif bool in args:
		idex = args.index(bool)
		return BoolParameterDescriptor(*(args[:idex]+args[idex+1:]), **kwargs)
	else: #Default behavior if not specified : a number, which is the more common parameter type in PlatRock.
		return FreeNumberParameterDescriptor(*args, **kwargs)

class ParameterDescriptor(object):
	"""
	Fully describes a parameter, useful for GUIs.
	
	Note:
		This class doesn't contain the value of the parameter, only its characteristics. Values are directly stored in instances, :class:`~Common.Simulations.GenericSimulation` for example.
	
	Attributes:
		input_names (list of strings || string): when reading platrock input parameters names from files, use this(ese) name(s) to bind to the right parameter. Always store as a list of strings in instances.
		inst_name (string): the instance name, name that this parameter will take in platrock source code, objects instances, etc...
		human_name (string): a human-readable and understandable full parameter name, including eventual unity
		type_ (type): the python type the parameter should be of
		min_value (:attr:`type_`): the minimum acceptable value
		max_value (:attr:`type_`): the maximum acceptable value
		default_value (:attr:`type_`): the default value
	"""

	def __init__(self,input_names,inst_name,human_name,type_,default_value):
		if not isinstance(input_names,list):
			input_names=[input_names]
		self.input_names=input_names
		self.inst_name=inst_name
		self.human_name=human_name
		self.type_=type_
		self.default_value=default_value

	def set_to_obj(self,obj,value=None,inst_name_prefix="",inst_name_suffix=""):
		"""
		Set a value from this parameter descriptor to an object attribute. This will cast to :attr:`type_` and set the :attr:`default_value` if the value given is None. The attribute name will be :attr:`inst_name`.
		
		Args:
			obj (object): the instance to set the parameter to
			value (anything castable to :attr:`type_`, optional): the value to set, if None :attr:`default_value` will be used
			inst_name_prefix (string, optional): a prefix added before :attr:`inst_name`
			inst_name_suffix (string, optional): a suffix added after :attr:`inst_name`
		"""
		if value==None:
			value=self.default_value
		if type(obj)==dict:
			obj[inst_name_prefix+self.inst_name+inst_name_suffix] = self.type_(value)
		else:
			setattr(obj,inst_name_prefix+self.inst_name+inst_name_suffix,self.type_(value))

class FreeNumberParameterDescriptor(ParameterDescriptor):
	TYPE = 'FreeNumber'
	def __init__(self,input_names,inst_name,human_name,type_,min_value=None,max_value=None,default_value=None):
		super().__init__(input_names, inst_name, human_name, type_, default_value)
		self.min_value=min_value
		self.max_value=max_value

class StringChoiceParameterDescriptor(ParameterDescriptor):
	TYPE = 'StringChoice'
	def __init__(self,input_names,inst_name,human_name,default_value="",choices=['']):
		super().__init__(input_names, inst_name, human_name, str, default_value)
		self.choices=choices

class FreeStringParameterDescriptor(ParameterDescriptor):
	TYPE = 'FreeString'
	def __init__(self,input_names,inst_name,human_name,default_value="",hint=False):
		super().__init__(input_names, inst_name, human_name, str, default_value)
		self.hint=hint

class BoolParameterDescriptor(ParameterDescriptor):
	TYPE = 'Bool'
	def __init__(self,input_names,inst_name,human_name,default_value=None):
		super().__init__(input_names, inst_name, human_name, bool, default_value)

class ParametersDescriptorsSet(object):
	"""
	A container of :class:`ParameterDescriptor`, with helper functions.
	
	Note:
		:class:`ParametersDescriptorsSet` are not iterable, use :attr:`parameters` attribute to loop on contained :class:`ParameterDescriptor`.
	
	Args:
		params_list (list of :class:`ParameterDescriptor` || list of list of args to construct :class:`ParameterDescriptor`): the input set of :class:`ParameterDescriptor`
		
	Attributes:
		parameters (list): contains the :class:`ParameterDescriptor`
		instance_names_to_parameters (dict): links :attr:`ParameterDescriptor.inst_name` to :class:`ParameterDescriptor`
		input_names_to_parameters (dict): links :attr:`ParameterDescriptor.input_names` to :class:`ParameterDescriptor`
		
	"""
	def __init__(self,params_list):
		self.parameters=[]
		self.instance_names_to_parameters={}
		self.input_names_to_parameters={}
		for p in params_list:
			if isinstance(p,ParameterDescriptor):
				self.add_parameter(p)
			else:
				self.add_parameter(*p)
	
	def __add__(self, other):
		new_obj=ParametersDescriptorsSet(self.parameters)
		for p in other.parameters:
			new_obj.add_parameter(p)
		return new_obj
	
	def __str__(self):
		replTable=[
			["<sub>"," :math:`_{"],
			["</sub>", "}` "],
			["<sup>"," :math:`^{"],
			["</sup>", "}` "],
		]
		L=[['instance name', 'input name(s)', 'human name']]
		for p in self.parameters:
			humName=p.human_name
			for repl in replTable:
				humName=humName.replace(*repl)
			l=[p.inst_name, ' || '.join(p.input_names), humName]
			L.append(l)
		return PyUtils.getRestructuredTextTableString(L)
	
	def add_parameter(self,*args,**kwargs):
		"""
		Adds a :class:`ParameterDescriptor` into this set, either by passing a :class:`ParametersDescriptorsSet` or args/kwargs that satisfies the :class:`ParameterDescriptor` constructor.
		
		Args:
			A single :class:`ParameterDescriptor`, or a set of arguments compatible with :class:`ParameterDescriptor` constructor signature.
		Kwargs:
			A set of keywords arguments compatible with :class:`ParameterDescriptor` constructor signature.
		"""
		if len(args)==1 and isinstance(args[0],ParameterDescriptor):
			new_param=args[0]
		else:
			new_param=parameterDescriptorFactory(*args,**kwargs)
		if(new_param.inst_name not in self.get_instance_names()): #avoid duplicates when adding (__add__) multiple ParametersDescriptorsSet
			self.parameters.append(new_param)
			self.instance_names_to_parameters[new_param.inst_name]=new_param
			for input_name in new_param.input_names:
				assert input_name not in self.input_names_to_parameters.keys()
				self.input_names_to_parameters[input_name]=new_param
			
	def get_param_by_input_name(self,input_name):
		"""
		Get a :class:`ParameterDescriptor` from its input name.
		
		Args:
			input_name (string): the input name to search for
		
		Returns:
			:class:`ParameterDescriptor` || bool: returns false if the param input name doesn't exist.
		"""
		return self.input_names_to_parameters.get(input_name,False)
	
	def get_param_by_instance_name(self,instance_name):
		"""
		Get a :class:`ParameterDescriptor` from its instance name.
		
		Args:
			instance_name (string): the instance name name to search for
		
		Returns:
			:class:`ParameterDescriptor` || bool: returns false if the param instance name doesn't exist.
		"""
		return self.instance_names_to_parameters.get(instance_name,False)
		
	def get_instance_names(self):
		"""
		Get all the instance names of the :class:`ParameterDescriptor` contained in this container
		
		Returns:
			list of strings
		"""
		return [p.inst_name for p in self.parameters]
	
	def get_human_names(self):
		"""
		Get all the human names of the :class:`ParameterDescriptor` contained in this container
		
		Returns:
			list of strings
		"""
		return [p.human_name for p in self.parameters]
	
	def get_input_names(self):
		"""
		Get all the input names of the :class:`ParameterDescriptor` contained in this container
		
		Returns:
			list of strings
		"""
		return list(self.input_names_to_parameters.keys())

def get_geojson_all_properties(filename,unique=True):
	"""
	Get all available "properties" names for all features of a geojson file.
	
	Args:
		filename (string): path to the geojson file
		unique (bool, optional): if set to False, all properties names of all features of the file will be output (2D list). If set to True the properties names of all features will be merged, but each parameter will appear once (1D list).
		
	Returns:
		list of strings
	"""
	result=[]
	shp_file=gdal.OpenEx(filename)
	for feat in shp_file.GetLayer(0):
		feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
		result.append(list(feat_dict['properties'].keys()))
	if unique:
		result=functools.reduce(operator.iconcat, result, []) #flatten
		unique_result = list(set(result))
		return unique_result
	return result

def get_geojson_all_shapes(filename,unique=True):
	"""
	Get all available "geometry" types for all features of a geojson file.
	
	Args:
		filename (string): path to the geojson file
		unique (bool, optional): if set to False, all geometry names of all features of the file will be output (2D list). If set to True the geometry names of all features will be merged, but each geometry will appear once (1D list).
		
	Returns:
		list of strings
	"""
	result=[]
	shp_file=gdal.OpenEx(filename)
	for feat in shp_file.GetLayer(0):
		feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
		result.append(feat_dict['geometry']["type"])
	if unique:
		#result=functools.reduce(operator.iconcat, result, []) #flatten
		unique_result = list(set(result))
		return unique_result
	return result

def extract_geojson_to_params_set(filename,destination,validation_params_descriptors_set,colormap):
	"""
	Get geometries and parameters from a geojson file, and populate the :attr:`destination` list.
	
	Note:
		The :attr:`destination` should be an instanciated list, for example as an object attribute, as it will be cleared then modified in place. Its format will be::
		
			[
			    {
			        "shapely_polygon": <the_corresponding_shapely_polygon_instance>,
			        "params": {
			            "R_n": 0.5,
			            "R_t": 0.2,
			            ...
			        },
			        "color": [0.5, 0.5, 0.5]
			    }
			]
	
	
	Args:
		filename (string): path to the geojson file
		destination (list): points to a list that will contains the parameters and geometries
		validation_params_descriptors_set (:class:`ParametersDescriptorsSet`): the parameters coming from the geojson file will be validated with this parameter container
		colormap (list): a (2D) list of rgb colors to set a "color" to each output parameter set
	
	Returns:
		0 if extraction is OK, the error message otherwise
	"""
	try:
		#self._geojson_polygon_soil_offset_applied=False
		shp_file=gdal.OpenEx(filename)
		destination.clear() # NOTE: don't overwrite destination pointer, use clear instead to keep the object in place.
		for feat in shp_file.GetLayer(0):
			feat_dict=feat.ExportToJson(as_object=True)
			destination.append({})
			shapely_poly = shapely.geometry.shape(feat_dict['geometry'])
			destination[-1]["shapely_polygon"]=shapely_poly
			if(isinstance(shapely_poly,shapely.geometry.MultiPolygon)): #we will have to choose later from the sub-polys, but ponderate by the poly areas. Build the area cumulative sum once here
					areas=np.asarray([p.area for p in list(shapely_poly.geoms)])	#areas of the polygons
					destination[-1]["multipoly_normalized_area_cumsum"]=np.cumsum(areas/sum(areas))
			destination[-1]["color"]=colormap[len(destination)-1]
			input_soil_params = feat_dict['properties']
			soil_params={}
			# SET THE DEFAULT PARAMS :
			for p in validation_params_descriptors_set.parameters:
				p.set_to_obj(soil_params)
			#validate the parameters from the input geojson and override the defaults
			for k in list(input_soil_params.keys()):
				param_descriptor = validation_params_descriptors_set.get_param_by_input_name(k)
				if param_descriptor:
					param_descriptor.set_to_obj(soil_params,input_soil_params[k])
			destination[-1]["params"]=soil_params
		return 0
	except Exception as e:
		message="Failed to import the geojson:"+str(e)
		Debug.error(message)
		return message

class Report(object):
	"""
	A report is a handy tool that groups a series of messages with corresponding message type. It is used to check users parameters in WebUI, before they launch a simulation.
	
	Attributes:
		nb_of_errors (int): counts the number of errors contained is this report
		messages (list): contains all the messages in the format [[mess_type, "the message"], ...]
	"""
	messages_letters_to_types={'I':'INFO','E':'ERROR','W':'WARNING'}
	"""
	Links between the message letter types (_type) and the corresponding human names
	"""
	
	def __init__(self):
		self.nb_of_errors=0
		self.messages=[]
	
	def add_message(self,_type,message):
		"""
		Adds a message to the report, should not really be used directly.
		
		Args:
			_type (sting): one of the :attr:`messages_letters_to_types` keys (for example "I")
			message (string): the message
		"""
		self.messages+=[[_type,message]]
	
	def add_info(self,message):
		"""
		Adds an info ("I") message to the report.
		
		Args:
			message (string): the message
		"""
		self.add_message('I',message)
	
	def add_error(self,message):
		"""
		Adds an error ("E") message to the report. Note that this will increment :attr:`nb_of_errors`.
		
		Args:
			message (string): the message
		"""
		self.nb_of_errors+=1
		self.add_message('E',message)
	
	def add_warning(self,message):
		"""
		Adds an warning ("W") message to the report.
		
		Args:
			message (string): the message
		"""
		self.add_message('W',message)
	
	def check_parameter(self,param_descriptor,param_value,location_string=""):
		"""
		Checks the validity of a value for a given :class:`ParameterDescriptor`. The value type and range will be checked, if they are not valid some error messages will be added to this report.
		
		Args:
			param_descriptor (:class:`ParameterDescriptor`): the parameter descriptor containing the type and range for the value
			param_value (any): the value to check
			location_string (string): for the error message to be more explicit, tell where the parameter comes from.
		"""
		if type(param_value)!=param_descriptor.type_:
			self.add_error( "In %s, %s is of invalid type (=%s but should be %s)."%(location_string,param_descriptor.inst_name, type(param_value).__name__, param_descriptor.type_.__name__) )
			return
		if param_value < param_descriptor.min_value or param_value > param_descriptor.max_value :
			self.add_error( "In %s, %s is not in its allowed range (=%s but should be within [%s,%s])."%(location_string,param_descriptor.inst_name, param_value, param_descriptor.min_value, param_descriptor.max_value) )
