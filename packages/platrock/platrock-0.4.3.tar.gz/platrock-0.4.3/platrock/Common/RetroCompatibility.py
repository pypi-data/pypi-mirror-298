import json,re,jsonpickle,types,inspect
import numpy as np
from . import Debug, Projects
import platrock

renamed_attrs=[
    {
        'py/object':'platrock.TwoD.Objects.Segment',
        'old':'dhp_mean',
        'new':'trees_dhp_mean'
    },
    {
        'py/object':'platrock.TwoD.Objects.Segment',
        'old':'dhp_std',
        'new':'trees_dhp_std'
    },
    {
        'py/object':'platrock.TwoD.Objects.Checkpoint',
        'old':'x',
        'new':'_x'
    },
    {
        'py/object':'platrock.TwoDShape.Objects.Checkpoint',
        'old':'x',
        'new':'_x'
    }
]
# import platrock.TwoD.Simulations
obj_cache={}
#     platrock.TwoD.Simulations.Simulation: # the class
#         platrock.TwoD.Simulations.Simulation( #the object
#             terrain=platrock.TwoD.Objects.Terrain(file=[
#                 'X Z bounce_model_number mu mu_r R_t R_n roughness v_half phi trees_density dhp_mean dhp_std',
#                 '0 300 0 0.5 0.3 0.8 0.7 0.31 5 30 200 30 10',
#                 '50 280 1 0.5 0.3 0.8 0.7 0.31 5 30 300 30 10'
#             ]),
#             checkpoints_x=[50]
#         )
# }
# if platrock.SICONOS_FOUND :
#     import platrock.TwoDShape.Simulations
#     obj_cache[platrock.TwoDShape.Simulations.Simulation] = platrock.TwoDShape.Simulations.Simulation(
#             terrain=platrock.TwoDShape.Objects.Terrain(file=[
#                 'X Z bounce_model_number mu mu_r R_t R_n roughness v_half phi trees_density dhp_mean dhp_std',
#                 '0 300 0 0.5 0.3 0.8 0.7 0.31 5 30 200 30 10',
#                 '50 280 1 0.5 0.3 0.8 0.7 0.31 5 30 300 30 10'
#             ]),
#             checkpoints_x=[50]
#         )

use_retro_compatibility=False

def rename_attrs(obj):
    global use_retro_compatibility
    for repl in renamed_attrs:
        if repl["py/object"] in obj.get("py/object","") and repl['old'] in obj.keys():
            obj[repl['new']]=obj[repl['old']]
            obj.pop(repl['old'])
            use_retro_compatibility=True
            Debug.warning("Replaced",repl['old'],'attr name by',repl['new'],"in an object of type",repl["py/object"])

def browse_and_rename_json(obj):
    if type(obj)==dict:
        rename_attrs(obj)
        for key,val in obj.items():
            browse_and_rename_json(val)
    elif type(obj)==list:
        for item in obj:
            browse_and_rename_json(item)

objs_already_seen=[]
def is_platrock_module(obj):
    return  (hasattr(obj, '__module__') and 
            re.match("^platrock\..*", obj.__module__) and 
            hasattr(obj,'__class__') and 
            not obj.__class__==type and #sometimes we store a class into platrock objects (obj)
            not obj.__class__==types.MethodType)  #for Engines "run" function which is bound dynamically.

# No longer needed, but keep it here just in case.
def is_instanciable_without_args(cls_):
    signature = inspect.signature(cls_.__init__)
    params = signature.parameters
    for p_name,param in params.items():
        if (param.name == 'self'):
            continue
        if (param.default is inspect._empty and param.kind is inspect._POSITIONAL_OR_KEYWORD):
            return False
    return True

def get_object(cls_):
    for cls_tree in cls_.mro(): #loop on cls_ ancestors, starting by cls_ itself.
        if ('_new_retro_compat_template' in cls_tree.__dict__):
            return cls_._new_retro_compat_template()
    return cls_()

def typecast(value, template):
    type_ = type(template)
    if (type_==np.ndarray):
        if (type(value)==list or type(value)==tuple):
            ret=np.asarray(value, dtype=template.dtype)
    else:
        ret=type_(value)
    return ret
        

def browse_and_complete_obj(obj, name = 'no_name'):
    global use_retro_compatibility, obj_cache
    # print('.......~~~~~~ Browse_and_complete_obj with',name,"=",obj,'at memory',hex(id(obj)))
    if type(obj)==dict:
        # print("The object is a dict, browse its",len(obj.values()),"values...")
        for key,value in obj.items():
            browse_and_complete_obj(value, key)
        # print("End of dict")
    elif type(obj)==list:
        # print("The object is a list, browse its",len(obj),"values...")
        for i,value in enumerate(obj):
            browse_and_complete_obj(value, '['+str(i)+']')
        # print("End of list")
    elif is_platrock_module(obj) and id(obj) not in objs_already_seen:
        # print("The object is a member of the platrock module named",obj.__module__)
        objs_already_seen.append(id(obj))
        if obj.__class__ in obj_cache.keys():
            template_obj = obj_cache[obj.__class__]
            # print("Object type template already in cache, use it",template_obj)
        else:
            template_obj = get_object(obj.__class__) # a new instance of the object, used as a template
            obj_cache[obj.__class__]=template_obj
            # print("Object type template has been created, use it",template_obj)
        for tmpl_attr_name,tmpl_attr_value in template_obj.__dict__.items():
            tmpl_attr_type = type(tmpl_attr_value)
            if not tmpl_attr_name in obj.__dict__.keys():
                Debug.warning("* * * * * * * Detected missing attr:",tmpl_attr_name,"in",obj,". Create it with default value",tmpl_attr_value)
                obj.__setattr__(tmpl_attr_name,tmpl_attr_value)
                use_retro_compatibility=True
            else:
                obj_attr_value = obj.__getattribute__(tmpl_attr_name)
                obj_attr_type = type(obj_attr_value)
                if obj_attr_type != tmpl_attr_type and tmpl_attr_value is not None:
                    if (tmpl_attr_type in [np.float64,float] and obj_attr_type in [np.float64,float]):
                        #Don't differenciate numpy.float64 and python float as its basically the same.
                        continue
                    Debug.warning("* * * * * * * Detected mistyped attr:",tmpl_attr_name,"=",obj_attr_value,"in",obj,"is",obj_attr_type,"but should be",tmpl_attr_type,". Try to typecast now...")
                    try:
                        new_val = typecast(obj_attr_value, tmpl_attr_value)
                        obj.__setattr__(tmpl_attr_name,new_val)
                        Debug.warning("Casting successful, new value is", obj_attr_value)
                    except Exception as e:
                        Debug.warning("Unable to typecast, change the value to",tmpl_attr_value)
                        Debug.warning("The error message was : "+str(e))
                        obj.__setattr__(tmpl_attr_name,tmpl_attr_value)
                        use_retro_compatibility=True
                else:
                    browse_and_complete_obj(obj_attr_value, tmpl_attr_name)
    # else:
    #     print("Nothing to do with that.")
    #else don't do anything, attr is present, non-object, non-list, non-dict, and same type as template

# def build_objs_cache():
#     global obj_cache, objs_already_seen
#     for class_,object_ in obj_cache.items():
#         browse_to_cache(object_)
#     objs_already_seen = []

# def browse_obj_to_cache(obj):
#     if type(obj)==dict:
#         for key,value in obj.items():
#             browse_to_cache(obj)
#     elif type(obj)==list:
#         for i,value in enumerate(obj):
#             browse_to_cache(obj)
#     elif is_platrock_module(obj) and id(obj) not in objs_already_seen:
#         objs_already_seen.append(id(obj))
#         for attr_name,attr_value in obj.__dict__.items():



def decode_legacy_json(json_string):
    """
    """
    global use_retro_compatibility
    js=json.loads(json_string)

    #FIRST HANDLE RENAMED ATTRS
    #IT IS NEEDED TO RESTORE VALUES OF RENAMED ATTRS
    #IT DIRECTLY WORKS ON THE JSON dict TREE.
    use_retro_compatibility=False
    browse_and_rename_json(js)
    #SECOND...
    obj = jsonpickle.decode(json.dumps(js),keys=True)
    if type(obj)==dict : #loading failed (no corresponding class found)
        return obj
    browse_and_complete_obj(obj)
    if(use_retro_compatibility):
        Debug.warning("Use retro compatibility.")
    obj.use_retro_compatibility=use_retro_compatibility

    return obj