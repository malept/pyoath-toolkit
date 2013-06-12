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

from .impl_cffi import OATH
import sys
import time

if sys.version_info < (2, 7):
    unittest_mod = 'unittest2'
else:
    unittest_mod = 'unittest'
unittest = __import__(unittest_mod)

DEFAULT_TIME_STEP_SIZE = 30
DIGITS = 6
WINDOW = 2


class CFFITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oath = OATH()

    def setUp(self):
        self.secret = self.oath.generate_secret_key('CFFITestCase secret')

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
        self.assertTrue(result)

    def test_hotp(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        otp2 = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        self.assertEqual(otp, otp2)
        otp3 = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        self.assertNotEqual(otp, otp3)
        result = self.oath.hotp_validate(self.secret, moving_factor,
                                         WINDOW, otp)
        self.assertTrue(result)

    def test_totp_fail(self):
        now = time.time()
        otp = self.oath.totp_generate(self.secret, now, None, 0, DIGITS)
        with self.assertRaises(RuntimeError):
            self.oath.totp_validate(self.secret, now, None, 60, WINDOW, otp)
