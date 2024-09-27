"""
"""

import io, quaternion
import numpy as np
from scipy import constants

from platrock.Common import Math, Debug

import siconos.kernel as sk
import siconos.numerics as sn
from siconos.io.mechanics_run import MechanicsHdf5Runner, MechanicsHdf5Runner_run_options
from siconos.mechanics.collision.tools import Contactor




class GenericShapeSimulation():
	"""
	Inherits from this class to add a Siconos layer to a simulation.
	"""
    
	class Siconos_Start_Run_Hook():
		def __init__(self, platrock_sim):
			pass

		def initialize(self, io):
			"""
			This will make siconos to run only the "setup" phase, without the actual run.
			"""
			self._io = io
			def return_false():
				return False
			self._io._simulation.hasNextEvent=return_false

		def call(self, step):
			pass

	def __init__(self):
		self.rocks_shape_params={} #for webui
		self.export_hdf5=False
		self.mechanicsHdf5Runner=None
		self.siconos_run_options=None
		self.current_DS=None
		self.last_record_pos=None

		#FIXME: study these values.
		self.inside_margin=0.03
		self.outside_margin=0.003
	
	def get_rock_cls_from_name(self,name):
		return self.get_parent_module().Objects.Rock.get_subclass_from_name(name)
	
	def record_condition(self):
		out = (self.last_record_pos-self.current_rock.pos).norm() > max(self.current_rock.dims)
		if out :
			self.last_record_pos=self.current_rock.pos[:]
		return out
	
	def init_siconos_mechanicsHdf5Runner(self):
		if self.export_hdf5 :
			hdf5_file = './siconos_out.hdf5'
		else:
			hdf5_file = io.BytesIO()
		#Following two lines emulates the classic "with MechanicsHdf5Runner() as io:" found in siconos scripts
		self.mechanicsHdf5Runner = MechanicsHdf5Runner(
			hdf5_file,
			verbose=False,
			io_filename_backup = "",
			gravity_scale=constants.g/self.gravity
		)
		self.mechanicsHdf5Runner.__enter__()
	
	def setup_siconos(self, solver_opts_class=None):
		options = sk.solver_options_create(solver_opts_class)
		options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = 10000
		options.dparam[sn.SICONOS_DPARAM_TOL] = 1e-4
		self.siconos_run_options = MechanicsHdf5Runner_run_options()
		self.siconos_run_options['T'] = 1e20 # total time
		self.siconos_run_options['h'] = self.dt
		self.siconos_run_options['Newton_max_iter'] = 10
		self.siconos_run_options['solver_options'] = options
		self.siconos_run_options['numerics_verbose'] = False
		self.siconos_run_options['verbose'] = False
		self.siconos_run_options['Newton_tolerance'] = 1e-4
		self.siconos_run_options['start_run_iteration_hook'] = self.Siconos_Start_Run_Hook(self)
		# self.siconos_run_options['Newton_options'] = sk.SICONOS_TS_LINEAR
		# self.siconos_run_options['skip_last_update_output'] = True
		# self.siconos_run_options['skip_reset_lambdas'] = True
		# self.siconos_run_options['osns_assembly_type'] = sk.REDUCED_DIRECT
		self.mechanicsHdf5Runner.run(self.siconos_run_options)
	
	def handle_hdf5_export(self):
		if self.export_hdf5 :
			self.mechanicsHdf5Runner.output_static_objects()
			self.mechanicsHdf5Runner.output_dynamic_objects()
			self.mechanicsHdf5Runner.output_velocities()
			self.mechanicsHdf5Runner.output_contact_forces()
			self.mechanicsHdf5Runner.output_solver_infos()
			# self.mechanicsHdf5Runner._out.flush()

	def add_siconos_rock(self):
		r=self.current_rock
		name = 'rock'+str(self.current_rock_number)
		translation=r.pos.tolist()
		if isinstance(r.ori,(list, tuple, np.ndarray)):
			orientation = r.ori
		elif isinstance(r.ori, quaternion.quaternion):
			orientation = [r.ori.w, r.ori.x, r.ori.y, r.ori.z]
		elif np.isscalar(r.ori):
			orientation = [r.ori]
		velocity=r.vel.tolist()+r.angVel.tolist()
		self.mechanicsHdf5Runner.add_convex_shape(
			name.capitalize(),
			self.current_rock.vertices,
			outsideMargin=self.outside_margin,
			insideMargin=self.inside_margin
		)
		self.mechanicsHdf5Runner.add_object(
			name,
			[
				Contactor(
					name.capitalize(),
					collision_group=0
				)
			],
			translation=translation,
			orientation=orientation,
			velocity=velocity,
			mass=r.mass,
			inertia = r.I,
			time_of_birth = self.mechanicsHdf5Runner.current_time()
		)
		
		self.mechanicsHdf5Runner.import_object(
			name=name,
			body_class=None,
			shape_class=None,
			face_class=None,
			edge_class=None,
			translation=translation,
			orientation=orientation,
			velocity=velocity,
			birth=True
		)

		self.current_DS = self.mechanicsHdf5Runner._nsds.dynamicalSystemsVector()[-1] #the last DS in siconos is the current rock.
	
	def remove_siconos_rock(self):
		self.mechanicsHdf5Runner._interman.removeBody(self.current_DS)
		self.mechanicsHdf5Runner._nsds.removeDynamicalSystem(self.current_DS)
		self.current_DS = None
	
	def before_run_tasks(self):
		self.init_siconos_mechanicsHdf5Runner()
		self.add_terrain()
		self.setup_siconos()
		self.last_record_pos=self.SPACE_VECTOR_CLASS()
		self.last_record_pos[:] = np.inf

	def before_rock_launch_tasks(self):
		self.add_siconos_rock()