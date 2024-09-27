"""
This module is used by PlatRock for logging. Log level can be set with `current_level` or by launching `platrock -ll=info` (replace `info` by the log level you want). It is also used by the WebUI to log to files instead of stdout.
"""

import multiprocessing,logging,sys,os,subprocess

#Message importance levels :
INFO=logging.INFO #20
"""
The more verbose mode.
"""
WARNING=logging.WARNING #30
"""
Intermediate verbosity.
"""
ERROR=logging.ERROR #40
"""
Only log errors
"""

#Actual log level : (log messages whose importance > current_level)
current_level=0
"""
Current log level. This is set by bin/platrock.
"""


def get_logger():
	"""
	Get the logger corresponding to the current process PID, or create one if it doesn't exist (this is the behavior of "logging.getLogger")
	
	Returns:
		:class:`logging.RootLogger`: the python logger to write into.
	"""
	return logging.getLogger(str(multiprocessing.current_process().pid))	#create a logger for this thread
	
def add_logger(filename=None):
	"""
	Get or create a logger based on the process PID, clear its handlers, add a new handler.
	
	Args:
		filename (string, optional): the filename to write into, otherwise log will output to stdout.
	"""
	logger = get_logger()	# get or create the logger
	logger.handlers=[]		# remove all the handlers
	if(filename==None or multiprocessing.current_process().name=='MainProcess'):
		handler = logging.StreamHandler()	#if the process is main (no multithreading, so no WebUI), log to console
	else: 
		if(os.path.exists(filename)): subprocess.call(["rm",filename])
		handler = logging.FileHandler(filename)									#if the process is a child, log to file
	logger.addHandler(handler)	#add the handler to the logger
	logger.propagate = False #avoid duplicate logging to the console
	logger.setLevel(current_level)
	logger.name="PlatRock-WebUI PID="+multiprocessing.current_process().name

def args_to_str(*args):
	"""
	Concatenate stringified variables.
	
	Args:
		*args (any): the arguments to be stringified.
		
	Returns:
		str: all args as strings, separated by spaces.
	"""
	S=""
	for arg in args:
		S+=str(arg)+" "
	return S

# Concatenate the input args, get the logger then log:
def info(*args):
	"""
	Write variables to current logger if the current log level is superior or equal to :attr:`INFO`.
	
	Args:
		*args (any): the variables to log.
	"""
	get_logger().info(args_to_str(*args))
	
def warning(*args):
	"""
	Write variables to current logger if the current log level is superior or equal to :attr:`WARNING`.
	
	Args:
		*args (any): the variables to log.
	"""
	get_logger().warning(args_to_str(*args))

def error(*args):
	"""
	Write variables to current logger if the current log level is superior or equal to :attr:`ERROR`.
	
	Args:
		*args (any): the variables to log.
	"""
	get_logger().error(args_to_str(*args))

def do_nothing(*args):
	pass

def init(level):
	"""
	This function sets the :attr:`current_level` and overrides the :meth:`info`, :meth:`warning`, :meth:`error` functions with :meth:`do_nothing` depending on the :attr:`level`.
	
	Args:
		level (int): the log level, should be set to :attr:`INFO`, :attr:`WARNING` or :attr:`ERROR`.
	"""
	global current_level
	current_level=level
	if(level>INFO):
		global info,Print
		info=do_nothing
		Print=do_nothing
	if(level>WARNING):
		global warning
		warning=do_nothing
	if(level>ERROR):
		global error
		error=do_nothing
