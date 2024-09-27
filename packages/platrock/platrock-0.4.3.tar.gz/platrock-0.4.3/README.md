# Description
PlatRock is a multi-model software for the numerical simulation of rockfalls. This scientific tool implements rock propagation algorithms on 2D and 3D terrain and gives statistical data about resulting trajectories.


# Prerequisites
At the moment PlatRock is only tested on debian-based platform unix distros. Prior to PlatRock installation, please check that the following dependencies are satisfied. 
* python >= 3.10, which is the default on modern linux distros ;
* [gdal](https://gdal.org/) (which can be installed on debian-based systems with `sudo apt install libgdal-dev`).

All other dependencies should be automatically installed by pip.

# Installation
Modern python package uses python virtual environments, so do PlatRock. You can use the virtual environment manager you want, below are two examples.

In any case, don't forget to install the `libgdal-dev` package as mentionned above.

## Using pipx
Install pipx on your disto:
> `sudo apt install pipx`

Then install PlatRock from pypi repository or gitlab:
> `pipx install platrock #the more stable release, from pipy`

or
> `pipx install git+https://gitlab.com/platrock/platrock.git@dev #the latest development banch, may be unstable`

You should normally be able to launch PlatRock by simply invoking it:
> `platrock myscript.py`

You can also import it in your own python script, but in this case you must activate the corresponding venv created by pipx before:
> `pipx list #shows all pipx venv created, find platrock venv path`

Usually, the command to activate PlatRock venv would be:
> `source "/home/$USER/.local/share/pipx/venvs/platrock/bin/activate"`

In your script:
> `import platrock`


## Using poetry
PlatRock uses poetry as packaging/dependency manager. You can install PlatRock using poetry. First install [poetry](https://python-poetry.org/docs/), and git.

Then download platrock:
> `git clone https://gitlab.com/platrock/platrock.git`

> `cd platrock`

Install PlatRock in ./.venv/:
> `poetry install`

Launch PlatRock:
> `poetry run platrock myscript.py`

Or import PlatRock from your own script, don't forget to activate PlatRock venv first:
> `poetry shell`

In your script:
> `import platrock`

# Examples
Examples for all PlatRock simulation models are available on [PlatRock gitlab](https://gitlab.com/platrock/platrock/-/tree/master/examples).
 

# Source code
The source code of platrock is also available on the [gitlab repository](https://gitlab.com/platrock/platrock). The master branch fits the version that is hosted on pypi.

# Licence
PlatRock is licenced under the GNU General Public License v3 (GPLv3).

# Contributors
* François Kneib
* Franck Bourrier
* David Toe
* Frédéric Berger
* Stéphane Lambert

