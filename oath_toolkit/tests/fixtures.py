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

from collections import namedtuple

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

DEFAULT_TIME_STEP_SIZE = 30
DIGITS = 6
WINDOW = 2

SECRET = b'TestCase secret'
OTK_SECRET = b'\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30' * 2

HOTP_VECTORS = (
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

TOTPG_VECTORS = (
    # From RFC 6238.
    TOTPGTestVector(59, 0x0000000000000001, b"94287082"),
    TOTPGTestVector(1111111109, 0x00000000023523EC, b"07081804"),
    TOTPGTestVector(1111111111, 0x00000000023523ED, b"14050471"),
    TOTPGTestVector(1234567890, 0x000000000273EF07, b"89005924"),
    TOTPGTestVector(2000000000, 0x0000000003F940AA, b"69279037"),
    TOTPGTestVector(20000000000, 0x0000000027BC86AA, b"65353130"),
)
TOTPV_VECTORS = (
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
