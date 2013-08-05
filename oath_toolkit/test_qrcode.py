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

from __future__ import absolute_import

from . import OATH, qrcode as oath_qrcode
from ._compat import url_quote
from .tests import unittest
import sys

# The tests crash on Python 2.6 and I don't know why
if (2, 7) <= sys.version_info:  # pragma: no cover
    import qrcode
else:  # pragma: no cover
    qrcode = None


@unittest.skipIf(qrcode is None,
                 'The qrcode module does not work in this version of Python')
class QRCodeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oath = OATH()

    def setUp(self):
        self.key = b'Hello!\xDE\xAD\xBE\xEF'
        self.secret = self.oath.generate_secret_key(self.key)

    def test_totp(self):
        expected_uri = '''\
otpauth://totp/Example:alice%40google.com?\
secret={0}&issuer=Example\
'''.format(url_quote(self.secret))
        expected_img = qrcode.make(expected_uri)
        expected = (self.secret, list(expected_img.getdata()))
        secret, img = oath_qrcode.generate(self.oath, 'totp', self.key,
                                           'alice@google.com', 'Example')
        self.assertEqual(expected, (secret, list(img.getdata())))

    def test_hotp(self):
        with self.assertRaises(ValueError):
            oath_qrcode.generate(self.oath, 'hotp', self.key,
                                 'alice@google.com', 'Example')
        expected_uri = '''\
otpauth://hotp/Example:alice%40google.com?\
secret={0}&issuer=Example&counter=42\
'''.format(url_quote(self.secret))
        expected_img = qrcode.make(expected_uri)
        expected = (self.secret, list(expected_img.getdata()))
        secret, img = oath_qrcode.generate(self.oath, 'hotp', self.key,
                                           'alice@google.com', 'Example', 42)
        self.assertEqual(expected, (secret, list(img.getdata())))
