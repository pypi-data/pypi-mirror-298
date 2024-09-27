# This script is used to cythonize PlatRock cython code.

import os
from setuptools import Distribution, Extension

from Cython.Build import build_ext, cythonize

# All PlatRock cython code is there:
cython_dir = os.path.join("platrock", "Cython")

# We use numpy dependency in cython
import numpy

# List here the cython files / PR modules
extensions = [
    Extension(
        "platrock.Common.ThreeDToolbox",
        [os.path.join(cython_dir, "ThreeDToolbox.pyx")],
        include_dirs=[numpy.get_include()]
    ),
    Extension(
        "platrock.Common.Math",
        [os.path.join(cython_dir, "Math.pyx")],
        include_dirs=[numpy.get_include()]
    )
]

ext_modules = cythonize(extensions, include_path=[cython_dir])
dist = Distribution({"ext_modules": ext_modules})
# "inplace" arg below will place the compiled .so files next to .py files, in the corresponding sub-package (ex: platrock/Common/Math.[...].so)
cmd = build_ext(dist, inplace=True)
cmd.ensure_finalized()
cmd.run()
