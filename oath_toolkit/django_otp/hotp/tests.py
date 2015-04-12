# -*- coding: utf-8 -*-
#
# Originally from django-otp 0.2.2:
# * django_otp/plugins/otp_hotp/tests.py
#
# Copyright (c) 2012, Peter Sagerson
# Copyright (c) 2014, 2015, Mark Lee
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from django.db import IntegrityError
from django_otp.tests import TestCase


class HOTPTest(TestCase):
    # The next three tokens
    tokens = [b'782373', b'313268', b'307722']

    def setUp(self):
        try:
            alice = self.create_user('alice', 'password')
        except IntegrityError:  # pragma: no cover
            self.skipTest("Unable to create test user.")
        else:
            self.device = alice.otoolkithotpdevice_set.create(
                secret_hex=b'd2e8a68036f68960b1c30532bb6c56da5934d879',
                digits=6, window=1, counter=0)

    def assert_token_verified(self, token):
        self.assertTrue(self.device.verify_token(token))
        self.assertEqual(self.device.counter, 1)

    def assert_token_not_verified(self, token):
        self.assertFalse(self.device.verify_token(token))
        self.assertEqual(self.device.counter, 0)

    def test_normal(self):
        self.assert_token_verified(self.tokens[0])

    def test_normal_drift(self):
        self.assert_token_verified(self.tokens[1])

    def test_excessive_drift(self):
        self.assert_token_not_verified(self.tokens[2])

    def test_bad_value(self):
        self.assert_token_not_verified(b'123456')
