"""

"""

from platrock.Common import Debug
import numpy as np


class GenericTimeSteppedSimulation():
	
	def __init__(self, dt=None):
		self.stop_vel_threshold = 0.2
		self.stop_acc_threshold = 0.5
		self.dt = dt
		self.current_rock_previous_vel = None
	
	def vel_acc_stop_condition(self):
		if self.current_rock_previous_vel is None:
			return False
		current_rock_accel_norm = (self.current_rock.vel-self.current_rock_previous_vel).norm()/self.dt
		if self.current_rock.vel.norm()<self.stop_vel_threshold and current_rock_accel_norm<self.stop_acc_threshold :
			return True
		return False
