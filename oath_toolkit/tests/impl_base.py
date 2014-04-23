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

from abc import ABCMeta
from collections import namedtuple
from itertools import chain
from platform import python_implementation
import sys
import time
from . import unittest
from ..exc import OATHError
from ..types import OTPPosition

skipIfPyPy = unittest.skipIf(python_implementation() == 'PyPy',
                             'XFAIL under PyPy')

DEFAULT_TIME_STEP_SIZE = 30
DIGITS = 6
WINDOW = 2

TOTPGTestVector = namedtuple('TOTPGTestVector', [
    'secs',
    'T',
    'otp',
])
TOTPVTestVector = namedtuple('TOTPVTestVector', [
    'now',
    'window',
    'otp',
    'expected_rc',
    'otp_pos',
    'otp_counter',  # not currently used
])


class OTPTestMixin(object):

    __metaclass__ = ABCMeta

    secret = b'TestCase secret'
    otk_secret = b'\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30' * 2
    hotp_vectors = (
        (),  # 0 digits
        (),  # 1 digit
        (),  # 2 digits
        (),  # 3 digits
        (),  # 4 digits
        (),  # 5 digits
        (  # 6 digits
            # The first ten of these match the values in RFC 4226.
            b"755224",
            b"287082",
            b"359152",
            b"969429",
            b"338314",
            b"254676",
            b"287922",
            b"162583",
            b"399871",
            b"520489",
            b"403154",
            b"481090",
            b"868912",
            b"736127",
            b"229903",
            b"436521",
            b"186581",
            b"447589",
            b"903435",
            b"578337",
        ),
        (  # 7 digits
            b"4755224",
            b"4287082",
            b"7359152",
            b"6969429",
            b"0338314",
            b"8254676",
            b"8287922",
            b"2162583",
            b"3399871",
            b"5520489",
            b"2403154",
            b"3481090",
            b"7868912",
            b"3736127",
            b"5229903",
            b"3436521",
            b"2186581",
            b"4447589",
            b"1903435",
            b"1578337",
        ),
        (  # 8 digits
            b"84755224",
            b"94287082",
            b"37359152",
            b"26969429",
            b"40338314",
            b"68254676",
            b"18287922",
            b"82162583",
            b"73399871",
            b"45520489",
            b"72403154",
            b"43481090",
            b"47868912",
            b"33736127",
            b"35229903",
            b"23436521",
            b"22186581",
            b"94447589",
            b"71903435",
            b"21578337",
        )
    )
    totpg_vectors = (
        # From RFC 6238.
        TOTPGTestVector(59, 0x0000000000000001, b"94287082"),
        TOTPGTestVector(1111111109, 0x00000000023523EC, b"07081804"),
        TOTPGTestVector(1111111111, 0x00000000023523ED, b"14050471"),
        TOTPGTestVector(1234567890, 0x000000000273EF07, b"89005924"),
        TOTPGTestVector(2000000000, 0x0000000003F940AA, b"69279037"),
        TOTPGTestVector(20000000000, 0x0000000027BC86AA, b"65353130"),
    )
    totpv_vectors = (
        # Derived from RFC 6238.
        TOTPVTestVector(0, 10, b"94287082", 1, 1, 1),
        TOTPVTestVector(1111111100, 10, b"07081804", 0, 0, 37037036),
        TOTPVTestVector(1111111109, 10, b"07081804", 0, 0, 37037036),
        TOTPVTestVector(1111111000, 10, b"07081804", 3, 3, 37037036),
        TOTPVTestVector(1111112000, 99, b"07081804", 30, -30, 37037036),
        TOTPVTestVector(1111111100, 10, b"14050471", 1, 1, 37037037),
        TOTPVTestVector(1111111109, 10, b"14050471", 1, 1, 37037037),
        TOTPVTestVector(1111111000, 10, b"14050471", 4, 4, 37037037),
        TOTPVTestVector(1111112000, 99, b"14050471", 29, -29, 37037037),
    )

    def assertEqualAtIndex(self, expected, actual, idx):
        msg = '{0} (expected) != {1} (actual) @ index {2}'
        self.assertEqual(expected, actual, msg.format(expected, actual, idx))

    def hotp_vector_iterate(self):
        for digits, otps in enumerate(self.hotp_vectors):
            for moving_factor, otp in enumerate(otps):
                yield digits, moving_factor, otp

    def verify_hotp_for_otk_tests(self, digits, counter, window, otp):
        raise NotImplementedError

    def assertGeneratedHOTPEqual(self, secret, moving_factor, digits, otp):
        raise NotImplementedError

    def assertGeneratedHOTPsFromOTK(self):
        self.assertGeneratedHOTPEqual(b'\x00', 1099511627776, 6, b'363425')

        for digits, moving_factor, otp in self.hotp_vector_iterate():
            self.assertGeneratedHOTPEqual(self.otk_secret, moving_factor,
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
        for i, tv in enumerate(self.totpg_vectors):
            if tv.secs > sys.maxsize:  # pragma: no cover
                # the timestamp is bigger than time_t for the arch, skip
                continue
            otp = self.generate_totp_for_otk_tests(tv.secs, digits, time_step)
            self.assertEqualAtIndex(tv.otp, otp, i)

    def verify_totp_for_otk_tests(self, time, time_step, window, otp):
        raise NotImplementedError

    def assertValidatedTOTPsFromOTK(self):
        time_step = 30
        for i, tv in enumerate(self.totpv_vectors):
            result = self.verify_totp_for_otk_tests(tv.now, time_step,
                                                    tv.window, tv.otp)
            self.assertIsInstance(result, OTPPosition)
            self.assertEqualAtIndex(tv.expected_rc, result.absolute, i)
            self.assertEqualAtIndex(tv.otp_pos, result.relative, i)


class ImplTestMixin(OTPTestMixin):

    def test_totp(self):
        now = time.time()
        time_step_size = None
        time_offset = 0
        otp = self.oath.totp_generate(self.secret, now, time_step_size,
                                      time_offset, DIGITS)
        self.assertEqual(DIGITS, len(otp))
        otp2 = self.oath.totp_generate(self.secret, now, time_step_size,
                                       time_offset, DIGITS)
        self.assertEqual(DIGITS, len(otp2))
        self.assertEqual(otp, otp2)
        otp3 = self.oath.totp_generate(self.secret, now, time_step_size,
                                       time_offset + DEFAULT_TIME_STEP_SIZE,
                                       DIGITS)
        self.assertEqual(DIGITS, len(otp3))
        self.assertNotEqual(otp, otp3)
        result = self.oath.totp_validate(self.secret, now, time_step_size,
                                         time_offset, WINDOW, otp)
        self.assertIsInstance(result, OTPPosition)
        self.assertGreaterEqual(result.absolute, 0)

    def generate_totp_for_otk_tests(self, time, digits, time_step):
        start_offset = 0
        return self.oath.totp_generate(self.otk_secret, time, time_step,
                                       start_offset, digits)

    @skipIfPyPy
    def test_totp_generate_from_otk_tests(self):
        self.assertGeneratedTOTPsFromOTK()

    def verify_totp_for_otk_tests(self, time, time_step, window, otp):
        start_offset = 0
        return self.oath.totp_validate(self.otk_secret, time, time_step,
                                       start_offset, window, otp)

    def test_totp_validate_from_otk_tests(self):
        self.assertValidatedTOTPsFromOTK()

    def test_hotp(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        self.assertEqual(DIGITS, len(otp))
        otp2 = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        self.assertEqual(DIGITS, len(otp2))
        self.assertEqual(otp, otp2)
        otp3 = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        self.assertEqual(DIGITS, len(otp3))
        self.assertNotEqual(otp, otp3)
        result = self.oath.hotp_validate(self.secret, moving_factor,
                                         WINDOW, otp)
        self.assertIsInstance(result, OTPPosition)
        self.assertIsNone(result.absolute)
        self.assertGreaterEqual(result.relative, 0)

    def assertGeneratedHOTPEqual(self, secret, moving_factor, digits, otp,
                                 add_checksum=False, truncation_offset=None):
        result = self.oath.hotp_generate(secret, moving_factor, digits,
                                         add_checksum, truncation_offset)
        idx = '[{0} Digits][Moving Factor {1}]'.format(digits, moving_factor)
        self.assertEqualAtIndex(otp, result, idx)

    @skipIfPyPy
    def test_hotp_generate_from_otk_tests(self):
        self.assertGeneratedHOTPsFromOTK()

        moving_factor = 0
        add_checksum = False
        truncation_offset = None
        for digits in chain(range(0, 6), range(9, 15)):
            with self.assertRaises(OATHError):
                self.oath.hotp_generate(self.otk_secret,
                                        moving_factor, digits,
                                        add_checksum,
                                        truncation_offset)

    def verify_hotp_for_otk_tests(self, digits, counter, window, otp):
        return self.oath.hotp_validate(self.otk_secret, counter,
                                       window, otp)

    def test_hotp_validate_from_otk_tests(self):
        self.assertValidatedHOTPsFromOTK()

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
