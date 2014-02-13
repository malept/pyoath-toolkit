#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013, 2014 Mark Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

from flake8.engine import get_style_guide
from flake8.main import print_report
from oath_toolkit import tests
import os
import sys

if sys.version_info < (2, 7):
    from unittest2 import TestLoader, TextTestRunner
else:
    from unittest import TestLoader, TextTestRunner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.dirname(tests.__file__)
BASE_UT_DIR = os.path.dirname(os.path.dirname(TESTS_DIR))


def main():
    # flake8
    flake8 = get_style_guide(exclude=['.tox', 'build'])
    report = flake8.check_files([BASE_DIR])

    exit_code = print_report(report, flake8)
    if exit_code > 0:
        return exit_code

    verbosity = 1
    if '--verbose' in sys.argv:
        verbosity += 1

    # oath_toolkit unit tests only
    # django_otp unit tests need to be run via Django's testrunner
    suite = TestLoader().discover(TESTS_DIR, top_level_dir=BASE_UT_DIR)
    result = TextTestRunner(verbosity=verbosity).run(suite)
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
