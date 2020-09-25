 #!/usr/bin/env python
import os
import re
import sys
import warnings
import versioneer
from setuptools import setup, find_packages
from numpy.distutils.core import setup, Extension
from numpy.distutils.fcompiler import get_default_fcompiler, CompilerNotFound

DISTNAME = 'xcape'
LICENSE = 'MIT'
AUTHOR = 'xcape Developers'
AUTHOR_EMAIL = 'rpa@ldeo.columbia.edu'
URL = 'https://github.com/xgcm/xcape'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering',
]

INSTALL_REQUIRES = ['xarray>=0.14.1', 'dask', 'numpy>=1.16']
PYTHON_REQUIRES = '>=3.6'

DESCRIPTION = "Fast convective parameters for numpy, dask, and xarray"
def readme():
    with open('README.rst') as f:
        return f.read()

# figure out which compiler we're going to use
compiler = get_default_fcompiler()
# set some fortran compiler-dependent flags
f90flags = []
if compiler == 'gnu95':
    f90flags.append('-fno-range-check')
    f90flags.append('-ffree-form')
elif compiler == 'intel' or compiler == 'intelem':
    f90flags.append('-132')
#  Set aggressive optimization level
f90flags.append('-O3')
#  Suppress all compiler warnings (avoid huge CI log files)
f90flags.append('-w')

ext_cape_ml = Extension(name = 'CAPE_CODE_model_lev',
                        sources = ['src/xcape/CAPE_CODE_model_lev.pyf',
                                   'src/xcape/CAPE_CODE_model_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_cape_pl = Extension(name = 'CAPE_CODE_pressure_lev',
                        sources = ['src/xcape/CAPE_CODE_pressure_lev.pyf',
                                   'src/xcape/CAPE_CODE_pressure_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_bunkers_ml = Extension(name = 'Bunkers_model_lev',
                        sources = ['src/xcape/Bunkers_model_lev.pyf',
                                   'src/xcape/Bunkers_model_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_bunkers_pl = Extension(name = 'Bunkers_pressure_lev',
                        sources = ['src/xcape/Bunkers_pressure_lev.pyf',
                                   'src/xcape/Bunkers_pressure_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_srh_ml = Extension(name = 'SREH_model_lev',
                        sources = ['src/xcape/SREH_model_lev.pyf',
                                   'src/xcape/SREH_model_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_srh_pl = Extension(name = 'SREH_pressure_lev',
                        sources = ['src/xcape/SREH_pressure_lev.pyf',
                                   'src/xcape/SREH_pressure_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_stdh_ml = Extension(name = 'stdheight_2D_model_lev',
                        sources = ['src/xcape/stdheight_2D_model_lev.pyf',
                                   'src/xcape/stdheight_2D_model_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])
ext_stdh_pl = Extension(name = 'stdheight_2D_pressure_lev',
                        sources = ['src/xcape/stdheight_2D_pressure_lev.pyf',
                                   'src/xcape/stdheight_2D_pressure_lev.f90'],
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'])

# https://github.com/readthedocs/readthedocs.org/issues/5512#issuecomment-475073310
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    ext_modules = []
    INSTALL_REQUIRES = []
else:
    ext_modules = [ext_cape_ml, ext_cape_pl,
                   ext_bunkers_ml, ext_bunkers_pl,
                   ext_srh_ml, ext_srh_pl,
                   ext_stdh_ml, ext_stdh_pl]

setup(name=DISTNAME,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license=LICENSE,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      classifiers=CLASSIFIERS,
      description=DESCRIPTION,
      long_description=readme(),
      install_requires=INSTALL_REQUIRES,
      python_requires=PYTHON_REQUIRES,
      url=URL,
      package_dir={"": "src"},
      packages=find_packages("src"),
      ext_package='xcape',
      ext_modules = ext_modules
      )
