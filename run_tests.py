#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Mark Lee
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

from flake8.main import check_file
import os
import sys

if sys.version_info < (2, 7):
    from unittest2 import TestLoader, TextTestRunner
else:
    from unittest import TestLoader, TextTestRunner

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, 'oath_toolkit')


def main():
    # flake8
    for root, dirs, files in os.walk(CODE_DIR):
        error_count = sum([check_file(os.path.join(root, f))
                           for f in files if f.endswith('.py')])
        if error_count > 0:
            print('Total Errors: {0}'.format(error_count), file=sys.stderr)
            return 1

    # unit tests
    suite = TestLoader().discover(CODE_DIR, top_level_dir=BASE_DIR)
    result = TextTestRunner().run(suite)
    if len(result.errors) > 0:
        return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main())
