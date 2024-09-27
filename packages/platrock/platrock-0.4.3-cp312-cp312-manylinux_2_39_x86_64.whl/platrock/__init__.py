name = "platrock"

from importlib import metadata
import os
version = metadata.version('platrock')

#Defaults to False, will be eventually overriden in platrock-webui:
web_ui = False

DATA_DIR = os.path.expanduser('~/.platrock')+'/'
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

# Install gdal:
# Note: GDAL can't be installed with poetry dependency system as its version must fit the version of the libgdal-dev system package.
import sys,subprocess
try:
    gdal_version = subprocess.check_output(["gdal-config","--version"]).decode().split('\n')[0]
except FileNotFoundError as E:
    print(E.args)
    print("gdal-config command cound not be found on this system. You must install it before launching PlatRock by invoking (adapt to your OS) 'sudo apt install libgdal-dev'")
    sys.exit(1)
try:
    import osgeo
    print("osgeo=="+osgeo.__version__+" python package was found.")
except ImportError as E:
    print(E.args)
    print('osgeo=='+gdal_version+' python package was not yet installed, try to install it now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'gdal[numpy]=='+gdal_version+'.*'])