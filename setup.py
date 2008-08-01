#! /usr/bin/env python

import sys
import os

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, Extension, find_packages
import distutils.util


install_requires=[]
execfile(distutils.util.convert_path('mwlib/_extversion.py')) 
# adds 'version' to local namespace

def read_long_description():
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.txt")
    return open(fn).read()

ext_modules = []
ext_modules.append(Extension("mwlib._rl_accel", ['mwlib/rl_addons/rl_accel/_rl_accel.c']))


setup(
    name="mwlib.ext",
    version=str(version),
    install_requires=install_requires,    
    packages=find_packages('.'),
    ext_modules=ext_modules,
    namespace_packages=['mwlib'],
    include_package_data = True,
    zip_safe = False,
    url = "http://code.pediapress.com/",
    description="provide dependencies for mwlib",
    license="BSD License",
    maintainer="pediapress.com",
    maintainer_email="info@pediapress.com",
    long_description = read_long_description()
)
