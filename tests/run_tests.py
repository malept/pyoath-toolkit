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

try:
    import argcomplete
except ImportError:
    argcomplete = None
import argparse
try:
    from django.core.management import execute_from_command_line
    django_installed = True
except ImportError:
    django_installed = False
try:
    from flake8.engine import get_style_guide
    from flake8.main import print_report
    flake8_installed = True
except ImportError:
    flake8_installed = False
from oath_toolkit import tests
import os
import sys

TestLoader = tests.unittest.TestLoader
TextTestRunner = tests.unittest.TextTestRunner

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(THIS_DIR)
TESTS_DIR = os.path.dirname(tests.__file__)
BASE_UT_DIR = os.path.dirname(os.path.dirname(TESTS_DIR))


def parse_args(prog, args):
    parser = argparse.ArgumentParser(prog)
    parser.add_argument('--no-flake8', dest='flake8', default=flake8_installed,
                        action='store_false', help='Disable Flake8')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Make unittest testrunner verbose')
    parser.add_argument('--no-django', dest='django', default=django_installed,
                        action='store_false',
                        help='Disable running the Django OTP device testsuite')
    parser.add_argument('--no-core-tests', dest='core', default=True,
                        action='store_false',
                        help='Disable running core tests')
    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser.parse_args(args)


def run_flake8():
    # flake8
    flake8 = get_style_guide(exclude=['.tox', 'build'])
    report = flake8.check_files([BASE_DIR])

    return print_report(report, flake8)


def run_core_tests(verbosity):
    suite = TestLoader().discover(TESTS_DIR, top_level_dir=BASE_UT_DIR)
    result = TextTestRunner(verbosity=verbosity).run(suite)
    if result.wasSuccessful():
        return 0
    else:
        return 1


def run_django_testrunner(prog, verbosity):
    # django_otp unit tests need to be run via Django's testrunner
    sys.path.append(THIS_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_django.settings'
    argv = [
        prog,
        'test',
        '--noinput',
        '--verbosity={0}'.format(verbosity),
        'oath_toolkit.django_otp.totp',
        'oath_toolkit.django_otp.hotp',
    ]
    execute_from_command_line(argv)


def main(argv):
    prog = argv[0]
    args = parse_args(prog, argv[1:])

    if args.flake8:
        exit_code = run_flake8()
        if exit_code > 0:
            return exit_code

    verbosity = 1
    if args.verbose:
        verbosity += 1

    # non-Django oath_toolkit unit tests only
    if args.core:
        exit_code = run_core_tests(verbosity)
        if exit_code > 0:
            return exit_code

    if args.django:
        run_django_testrunner(prog, verbosity)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
