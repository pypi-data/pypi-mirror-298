#!/usr/bin/python3

"""
PlatRock main executable script.
"""
import os,argparse,traceback

def main():


	from IPython.terminal.embed import InteractiveShellEmbed
	shell = InteractiveShellEmbed()
	shell.enable_matplotlib()


	parser = argparse.ArgumentParser()
	parser.add_argument("-ll", "--log-level", dest="log_level", help="Log level", choices=['info', 'warning', 'error'],default='warning')
	parser.add_argument("input_script", nargs='?', help="The script to launch.", default=None)
	args = parser.parse_args()

	bin_file=os.path.realpath(__file__)

	import platrock
	import platrock.Common.Debug as Debug
	from platrock.Common.PyUtils import colorPythonError

	from platrock import TwoD # to be able to use TwoD.[...] in scripts
	import platrock.TwoD.Simulations, platrock.TwoD.Objects

	from platrock import ThreeD # to be able to use ThreeD.[...] in scripts
	import platrock.ThreeD.Simulations, platrock.ThreeD.Objects

	try:
		from platrock import TwoDShape
		import platrock.TwoDShape.Simulations, platrock.TwoDShape.Objects
		from platrock import ThreeDShape
		import platrock.ThreeDShape.Simulations, platrock.ThreeDShape.Objects
		platrock.SICONOS_FOUND = True
	except:
		print("All -shape models are disabled as siconos importation failed. The error was :")
		print(colorPythonError(traceback.format_exc()))
		platrock.SICONOS_FOUND = False

	if(args.log_level=='info'):
		Debug.init(Debug.INFO)
	elif(args.log_level=='warning'):
		Debug.init(Debug.WARNING)
	elif(args.log_level=='error'):
		Debug.init(Debug.ERROR)
	Debug.add_logger()

	print("Launching PlatRock",platrock.version)
	if(args.input_script==None):
		print("No script given.")
	elif os.path.exists(args.input_script):
		path = os.path.abspath(args.input_script)
		try:
			exec(open(path).read())
		except:
			print(colorPythonError(traceback.format_exc()))
	else:
		print("Cannot find " + args.input_script)
		os._exit(1)
	shell()
