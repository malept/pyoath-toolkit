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

from platform import python_implementation
try:  # pragma: no cover
    from ..impl_cffi import oath
except ImportError:  # pragma: no cover
    oath = None
from . import unittest
from .impl_base import ImplTestMixin

skipIfPyPy = unittest.skipIf(python_implementation() == 'PyPy',
                             'XFAIL under PyPy')


@unittest.skipIf(oath is None, 'Could not import CFFI implementation')
class CFFITestCase(ImplTestMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oath = oath

    def test_library_version(self):
        version = super(CFFITestCase, self).test_library_version()
        self.assertNotEqual(self.oath._ffi.NULL, version)

    test_totp_generate_from_otk_tests = \
        skipIfPyPy(ImplTestMixin.test_totp_generate_from_otk_tests)
