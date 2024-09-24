import os
import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()

pycmox = Pybind11Extension('pycmox',
    sources = ['src/pycmox.cpp', 'src/infras/exchange.cpp'],
    cxx_std = 11,
    include_dirs = ['src/infras'],
    define_macros = [('NO_RS485_LEGACY', None)])

setup(
	name='pycmox',
	version='0.2.2',
	packages=[],
	ext_modules=[pycmox],
	include_package_data=True,
	license='LGPL-3.0-or-later',
	description='A Python wrapper for lmox',
	long_description=README,
	url='https://curl.sai.msu.ru/hg/pycmox/',
	author='Matwey V. Kornilov',
	author_email='matwey.kornilov@gmail.com',
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
	]
)
