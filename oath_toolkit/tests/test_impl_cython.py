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

from .impl_base import ImplTestMixin
try:  # pragma: no cover
    from ..impl_cython import oath
except ImportError:  # pragma: no cover
    oath = None
from . import unittest


@unittest.skipIf(oath is None, 'Could not import Cython implementation')
class CythonTestCase(ImplTestMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oath = oath
