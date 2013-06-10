#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as f:
    description = f.read()

setup(name='oath_toolkit',
      version='1.0',
      description='Python bindings for OATH Toolkit',
      long_description=description,
      author='Mark Lee',
      packages=['oath_toolkit'],
      install_requires=['cffi'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ])
