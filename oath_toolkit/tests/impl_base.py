# -*- coding: utf-8 -*-
#
# Copyright 2013, 2014, 2015 Mark Lee
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

from abc import ABCMeta
from itertools import chain
from platform import python_implementation
import sys
import time
from . import unittest
from ..exc import OATHError
from .fixtures import (
    DEFAULT_TIME_STEP_SIZE, DIGITS, HOTP_VECTORS, OTK_SECRET, SECRET,
    TOTPG_VECTORS, TOTPV_VECTORS, WINDOW)
from ..types import OTPPosition

skipIfPyPy = unittest.skipIf(python_implementation() == 'PyPy',
                             'XFAIL under PyPy')


class OTPTestMixin(object):

    __metaclass__ = ABCMeta

    def assertEqualAtIndex(self, expected, actual, idx):
        msg = '{0} (expected) != {1} (actual) @ index {2}'
        self.assertEqual(expected, actual, msg.format(expected, actual, idx))

    def hotp_vector_iterate(self):
        for digits, otps in enumerate(HOTP_VECTORS):
            for moving_factor, otp in enumerate(otps):
                yield digits, moving_factor, otp

    def verify_hotp_for_otk_tests(self, digits, counter, window, otp):
        raise NotImplementedError

    def assertGeneratedHOTPEqual(self, secret, moving_factor, digits, otp):
        raise NotImplementedError

    def assertGeneratedHOTPsFromOTK(self):
        self.assertGeneratedHOTPEqual(b'\x00', 1099511627776, 6, b'363425')

        for digits, moving_factor, otp in self.hotp_vector_iterate():
            self.assertGeneratedHOTPEqual(OTK_SECRET, moving_factor,
                                          digits, otp)

    def assertValidatedHOTPsFromOTK(self):
        counter = 0
        window = 20
        for digits, moving_factor, otp in self.hotp_vector_iterate():
            result = self.verify_hotp_for_otk_tests(digits, counter, window,
                                                    otp)
            self.assertIsInstance(result, OTPPosition)
            self.assertEqualAtIndex(moving_factor, result.relative, digits)

    def generate_totp_for_otk_tests(self, time, digits, time_step):
        raise NotImplementedError

    def assertGeneratedTOTPsFromOTK(self):
        time_step = 30
        digits = 8
        for i, tv in enumerate(TOTPG_VECTORS):
            if tv.secs > sys.maxsize:  # pragma: no cover
                # the timestamp is bigger than time_t for the arch, skip
                continue
            otp = self.generate_totp_for_otk_tests(tv.secs, digits, time_step)
            self.assertEqualAtIndex(tv.otp, otp, i)

    def verify_totp_for_otk_tests(self, time, time_step, window, otp):
        raise NotImplementedError

    def assertValidatedTOTPsFromOTK(self):
        time_step = 30
        for i, tv in enumerate(TOTPV_VECTORS):
            result = self.verify_totp_for_otk_tests(tv.now, time_step,
                                                    tv.window, tv.otp)
            self.assertIsInstance(result, OTPPosition)
            self.assertEqualAtIndex(tv.expected_rc, result.absolute, i)
            self.assertEqualAtIndex(tv.otp_pos, result.relative, i)


class ImplTestMixin(OTPTestMixin):

    def test_totp(self):
        now = time.time()
        time_step_size = -1
        time_offset = 0
        otp = self.oath.totp_generate(SECRET, now, time_step_size,
                                      time_offset, DIGITS)
        self.assertEqual(DIGITS, len(otp))
        otp2 = self.oath.totp_generate(SECRET, now, time_step_size,
                                       time_offset, DIGITS)
        self.assertEqual(DIGITS, len(otp2))
        self.assertEqual(otp, otp2)
        otp3 = self.oath.totp_generate(SECRET, now, time_step_size,
                                       time_offset + DEFAULT_TIME_STEP_SIZE,
                                       DIGITS)
        self.assertEqual(DIGITS, len(otp3))
        self.assertNotEqual(otp, otp3)
        result = self.oath.totp_validate(SECRET, now, time_step_size,
                                         time_offset, WINDOW, otp)
        self.assertIsInstance(result, OTPPosition)
        self.assertGreaterEqual(result.absolute, 0)

    def generate_totp_for_otk_tests(self, time, digits, time_step):
        start_offset = 0
        return self.oath.totp_generate(OTK_SECRET, time, time_step,
                                       start_offset, digits)

    @skipIfPyPy
    def test_totp_generate_from_otk_tests(self):
        self.assertGeneratedTOTPsFromOTK()

    def verify_totp_for_otk_tests(self, time, time_step, window, otp):
        start_offset = 0
        return self.oath.totp_validate(OTK_SECRET, time, time_step,
                                       start_offset, window, otp)

    def test_totp_validate_from_otk_tests(self):
        self.assertValidatedTOTPsFromOTK()

    def test_hotp(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(SECRET, moving_factor, DIGITS,
                                      False, -1)
        self.assertEqual(DIGITS, len(otp))
        otp2 = self.oath.hotp_generate(SECRET, moving_factor, DIGITS,
                                       False, -1)
        self.assertEqual(DIGITS, len(otp2))
        self.assertEqual(otp, otp2)
        otp3 = self.oath.hotp_generate(SECRET, moving_factor + 1, DIGITS,
                                       False, -1)
        self.assertEqual(DIGITS, len(otp3))
        self.assertNotEqual(otp, otp3)
        result = self.oath.hotp_validate(SECRET, moving_factor,
                                         WINDOW, otp)
        self.assertIsInstance(result, OTPPosition)
        self.assertIsNone(result.absolute)
        self.assertGreaterEqual(result.relative, 0)

    def assertGeneratedHOTPEqual(self, secret, moving_factor, digits, otp,
                                 add_checksum=False, truncation_offset=-1):
        result = self.oath.hotp_generate(secret, moving_factor, digits,
                                         add_checksum, truncation_offset)
        idx = '[{0} Digits][Moving Factor {1}]'.format(digits, moving_factor)
        self.assertEqualAtIndex(otp, result, idx)

    @skipIfPyPy
    def test_hotp_generate_from_otk_tests(self):
        self.assertGeneratedHOTPsFromOTK()

        moving_factor = 0
        add_checksum = False
        truncation_offset = -1
        for digits in chain(range(0, 6), range(9, 15)):
            with self.assertRaises(OATHError):
                self.oath.hotp_generate(OTK_SECRET, moving_factor, digits,
                                        add_checksum, truncation_offset)

    def verify_hotp_for_otk_tests(self, digits, counter, window, otp):
        return self.oath.hotp_validate(OTK_SECRET, counter, window, otp)

    def test_hotp_validate_from_otk_tests(self):
        self.assertValidatedHOTPsFromOTK()

    def test_hotp_fail(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(SECRET, moving_factor + 1, DIGITS,
                                      False, -1)
        with self.assertRaises(OATHError):  # outside of window
            self.oath.hotp_validate(SECRET, moving_factor, 0, otp)

    def test_totp_fail(self):
        now = time.time()
        otp = self.oath.totp_generate(SECRET, now, 30, 0, DIGITS)
        with self.assertRaises(OATHError):  # outside of window
            self.oath.totp_validate(SECRET, now + 60, -1, 30, 0, otp)

    def test_library_version(self):
        version = self.oath.library_version
        self.assertIsNotNone(version)
        return version

    def test_check_library_version(self):
        self.assertTrue(self.oath.check_library_version(b'0'))
        self.assertFalse(self.oath.check_library_version(b'999'))

    def test_base32_decode(self):
        # From oath-toolkit, liboath/tests/tst_coding.c
        with self.assertRaises((OATHError, TypeError)):
            self.oath.base32_decode(None)
        with self.assertRaises((OATHError, TypeError)):
            self.oath.base32_decode(b'*')
        self.assertEqual(b'foo', self.oath.base32_decode(b'MZXW6==='))
