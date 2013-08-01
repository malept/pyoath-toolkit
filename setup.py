#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup
import sys

os.environ['SETUP_NO_CFFI'] = '1'

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from oath_toolkit import metadata

del os.environ['SETUP_NO_CFFI']

with open('README.rst') as f:
    long_description = f.read()

setup(name='oath_toolkit',
      version=metadata.VERSION,
      description=metadata.DESCRIPTION,
      long_description=long_description,
      author='Mark Lee',
      author_email='pyoath-toolkit@lazymalevolence.com',
      url='https://github.com/malept/pyoath-toolkit',
      packages=['oath_toolkit'],
      install_requires=['cffi'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
