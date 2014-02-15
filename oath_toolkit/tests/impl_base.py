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

import time
from ..exc import OATHError

DEFAULT_TIME_STEP_SIZE = 30
DIGITS = 6
WINDOW = 2


class ImplTestMixin(object):

    def setUp(self):
        self.secret = b'TestCase secret'

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
        self.assertGreaterEqual(result, 0)

    def test_hotp(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        otp2 = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        self.assertEqual(otp, otp2)
        otp3 = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        self.assertNotEqual(otp, otp3)
        result = self.oath.hotp_validate(self.secret, moving_factor,
                                         WINDOW, otp)
        self.assertGreaterEqual(result, 0)

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
