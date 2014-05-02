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

from __future__ import absolute_import

from .. import qrcode as oath_qrcode
from .._compat import url_quote
from . import unittest
import qrcode
import sys

skipIfPy34 = unittest.skipIf(sys.version_info[:2] == (3, 4),
                             'Skipping on Python 3.4')


@skipIfPy34
class QRCodeTestCase(unittest.TestCase):

    def setUp(self):
        self.key = b'Hello!\xDE\xAD\xBE\xEF'
        self.secret = b'JBSWY3DPEHPK3PXP'

    def test_totp(self):
        expected_uri = '''\
otpauth://totp/Example:alice%40google.com?\
secret={0}&issuer=Example\
'''.format(url_quote(self.secret))
        expected_img = qrcode.make(expected_uri)
        expected = list(expected_img.getdata())
        img = oath_qrcode.generate('totp', self.key,
                                   'alice@google.com', 'Example')
        self.assertEqual(expected, list(img.getdata()))

    def test_hotp(self):
        with self.assertRaises(ValueError):
            oath_qrcode.generate('hotp', self.key,
                                 'alice@google.com', 'Example')
        expected_uri = '''\
otpauth://hotp/Example:alice%40google.com?\
secret={0}&issuer=Example&counter=42\
'''.format(url_quote(self.secret))
        expected_img = qrcode.make(expected_uri)
        expected = list(expected_img.getdata())
        img = oath_qrcode.generate('hotp', self.key,
                                   'alice@google.com', 'Example', 42)
        self.assertEqual(expected, list(img.getdata()))
