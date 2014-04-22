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

import hashlib
from .. import HOTP, OATH, TOTP
from ..exc import OATHError
from . import unittest
from . import impl_base


class OTPTestMixin(impl_base.OTPTestMixin):

    def test_algorithm(self):
        algorithm = hashlib.sha1
        otp = self.create_otp(algorithm)
        self.assertEqual(algorithm, otp.algorithm)
        with self.assertRaises(ValueError):
            self.create_otp(hashlib.md5)


class HOTPTestCase(OTPTestMixin, unittest.TestCase):

    """Tests the implementation-agnostic HOTP class."""

    def create_otp(self, algorithm):
        return HOTP(b'\x01', 6, algorithm)

    def assertGeneratedHOTPEqual(self, secret, counter, digits, otp):
        hotp = HOTP(secret, digits)
        result = hotp.generate(counter)
        idx = '[{0} Digits][Moving Factor {1}]'.format(digits, counter)
        self.assertEqualAtIndex(otp, result, idx)

    def verify_hotp_for_otk_tests(self, digits, counter, window, otp):
        hotp = HOTP(self.otk_secret, digits)
        return hotp.verify(otp, counter, window)

    @impl_base.skipIfPyPy
    def test_generate_from_otk_tests(self):
        self.assertGeneratedHOTPsFromOTK()

    def test_verify_from_otk_tests(self):
        self.assertValidatedHOTPsFromOTK()


class TOTPTestCase(OTPTestMixin, unittest.TestCase):

    """Tests the implementation-agnostic TOTP class."""

    def create_otp(self, algorithm):
        return TOTP(b'\x01', 6, 30, algorithm)

    @impl_base.skipIfPyPy
    def generate_totp_for_otk_tests(self, time, digits, time_step):
        totp = TOTP(self.otk_secret, digits, time_step)
        return totp.generate(time)

    def verify_totp_for_otk_tests(self, time, time_step, window, otp):
        totp = TOTP(self.otk_secret, None, time_step)
        return totp.verify(otp, time, window)

    def test_generate_from_otk_tests(self):
        self.assertGeneratedTOTPsFromOTK()

    def test_verify_from_otk_tests(self):
        self.assertValidatedTOTPsFromOTK()


class OATHTestCase(impl_base.ImplTestMixin, unittest.TestCase):

    """Tests the implementation-agnostic class."""

    @classmethod
    def setUpClass(cls):
        cls.oath = OATH()

    def test_base32_decode(self):
        # From oath-toolkit, liboath/tests/tst_coding.c
        with self.assertRaises((OATHError, TypeError)):
            self.oath.base32_decode(b'')
        with self.assertRaises((OATHError, TypeError)):
            self.oath.base32_decode(b'NIXnix')
        self.assertEqual(b'foo', self.oath._py_base32_decode(b'MZ XW 6'))
        self.assertEqual(b'foo', self.oath._py_base32_decode(b'MZ XW 6==='))
        dropbox = b'gr6d 5br7 25s6 vnck v4vl hlao re'
        self.assertEqual(16, len(self.oath._py_base32_decode(dropbox)))
        super(OATHTestCase, self).test_base32_decode()

    def test_base32_encode(self):
        # From oath-toolkit, liboath/tests/tst_coding.c
        self.assertEqual(b'', self.oath.base32_encode(None))
        self.assertEqual(b'', self.oath.base32_encode(b''))
        self.assertEqual(b'MZXW6===', self.oath.base32_encode(b'foo'))
        base32_encoded = self.oath.base32_encode(b'foo',
                                                 human_readable=True)
        self.assertEqual(b'MZXW 6', base32_encoded)
