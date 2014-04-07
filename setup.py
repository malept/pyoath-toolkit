#!/usr/bin/env python
# -*- coding: utf-8 -*-

####
# Dirty Monkeypatching Hacks
####

# distutils sdist for Vagrant
#
# Allow distutils sdist to work correctly when using Vagrant + VirtualBox
# shared folders, where hard links are not implemented.
#
# See also: http://bugs.python.org/msg208792

import os
import sys

if 'sdist' in sys.argv and os.environ.get('USER', '') == 'vagrant':
    if hasattr(os, 'link'):
        del os.link

####
# Your regularly scheduled setup file
####

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None
import os
from platform import python_implementation
import re
from setuptools import find_packages, setup
from setuptools.extension import Extension
import sys

os.environ['SETUP_PY'] = '1'

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from oath_toolkit import metadata

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

RE_REQ_COMMENT = re.compile(r'#.*$')


def requires_from_req_txt(filename):
    requires = []
    with open(filename) as f:
        for line in f:
            req = RE_REQ_COMMENT.sub('', line).strip()
            if req != '':
                requires.append(req)
    return requires

with open('README.rst') as f:
    long_description = f.read()

requires = []
if not os.environ.get('READTHEDOCS'):
    requires = requires_from_req_txt('requirements.txt')
extra_req = dict([(x, requires_from_req_txt('requirements-{0}.txt'.format(x)))
                  for x in ['django-otp', 'qrcode', 'wtforms']])

attrs = dict(name='pyoath-toolkit',
             version=metadata.VERSION,
             description=metadata.DESCRIPTION,
             long_description=long_description,
             author='Mark Lee',
             author_email='pyoath-toolkit@lazymalevolence.com',
             url='https://pyoath-toolkit.readthedocs.org/',
             packages=find_packages(),
             install_requires=requires,
             extras_require=extra_req,
             classifiers=CLASSIFIERS)

SANS_CYTHON_FLAG = '--without-cython'
sans_cython_flag_exists = SANS_CYTHON_FLAG in sys.argv
with_cython = (python_implementation() != 'PyPy' and
               not sans_cython_flag_exists)
if with_cython:
    src_ext = 'pyx' if cythonize else 'c'
    ext = Extension('oath_toolkit.impl_cython',
                    ['oath_toolkit/impl_cython.{0}'.format(src_ext)],
                    libraries=['oath'])
    if cythonize:
        directives = {
            'language_level': sys.version_info[0],
        }
        attrs['ext_modules'] = cythonize([ext], compiler_directives=directives)
    else:
        attrs['ext_modules'] = [ext]
elif sans_cython_flag_exists:
    sys.argv.remove(SANS_CYTHON_FLAG)

setup(**attrs)
