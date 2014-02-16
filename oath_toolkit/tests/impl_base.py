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

from collections import namedtuple
import time
from ..exc import OATHError
from ..types import OTPPosition

DEFAULT_TIME_STEP_SIZE = 30
DIGITS = 6
WINDOW = 2

TestVector = namedtuple('TestVector', [
    'now',
    'window',
    'otp',
    'expected_rc',
    'otp_pos',
    'otp_counter',  # not currently used
])


class ImplTestMixin(object):

    def setUp(self):
        self.secret = b'TestCase secret'
        self.otk_secret = b'\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30' * 2
        self.tvectors_totp = [
            # Derived from RFC 6238.
            TestVector(0, 10, b"94287082", 1, 1, 1),
            TestVector(1111111100, 10, b"07081804", 0, 0, 37037036),
            TestVector(1111111109, 10, b"07081804", 0, 0, 37037036),
            TestVector(1111111000, 10, b"07081804", 3, 3, 37037036),
            TestVector(1111112000, 99, b"07081804", 30, -30, 37037036),
            TestVector(1111111100, 10, b"14050471", 1, 1, 37037037),
            TestVector(1111111109, 10, b"14050471", 1, 1, 37037037),
            TestVector(1111111000, 10, b"14050471", 4, 4, 37037037),
            TestVector(1111112000, 99, b"14050471", 29, -29, 37037037),
        ]

    def test_totp(self):
        now = time.time()
        time_step_size = None
        time_offset = 0
        otp = self.oath.totp_generate(self.secret, now, time_step_size,
                                      time_offset, DIGITS)
        otp2 = self.oath.totp_generate(self.secret, now, time_step_size,
                                       time_offset, DIGITS)
        self.assertEqual(otp, otp2)
        otp3 = self.oath.totp_generate(self.secret, now, time_step_size,
                                       time_offset + DEFAULT_TIME_STEP_SIZE,
                                       DIGITS)
        self.assertNotEqual(otp, otp3)
        result = self.oath.totp_validate(self.secret, now, time_step_size,
                                         time_offset, WINDOW, otp)
        self.assertIsInstance(result, OTPPosition)
        self.assertGreaterEqual(result.absolute, 0)

    def assertEqualAtIndex(self, expected, actual, idx):
        msg = '{0} (expected) != {1} (actual) @ index {2}'
        self.assertEqual(expected, actual, msg.format(expected, actual, idx))

    def test_totp_validate_from_otk_tests(self):
        time_step_size = None
        start_offset = 0
        for i, tv in enumerate(self.tvectors_totp):
            result = self.oath.totp_validate(self.otk_secret, tv.now,
                                             time_step_size, start_offset,
                                             tv.window, tv.otp)
            self.assertIsInstance(result, OTPPosition)
            self.assertEqualAtIndex(tv.expected_rc, result.absolute, i)
            self.assertEqualAtIndex(tv.otp_pos, result.relative, i)

    def test_hotp(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        otp2 = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        self.assertEqual(otp, otp2)
        otp3 = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        self.assertNotEqual(otp, otp3)
        result = self.oath.hotp_validate(self.secret, moving_factor,
                                         WINDOW, otp)
        self.assertIsInstance(result, OTPPosition)
        self.assertIsNone(result.absolute)
        self.assertGreaterEqual(result.relative, 0)

    def test_hotp_fail(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        with self.assertRaises(OATHError):  # outside of window
            self.oath.hotp_validate(self.secret, moving_factor, 0, otp)

    def test_totp_fail(self):
        now = time.time()
        otp = self.oath.totp_generate(self.secret, now, 30, 0, DIGITS)
        with self.assertRaises(OATHError):  # outside of window
            self.oath.totp_validate(self.secret, now + 60, None, 30, 0, otp)

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
