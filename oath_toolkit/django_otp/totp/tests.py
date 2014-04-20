# -*- coding: utf-8 -*-
#
# Originally from django-otp 0.2.2:
# * django_otp/plugins/otp_totp/tests.py
#
# Copyright (c) 2012, Peter Sagerson
# Copyright (c) 2014, Mark Lee
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
from django.test.client import RequestFactory
from django_otp.tests import TestCase
from qrcode.image.base import BaseImage
from time import time
from .models import OToolkitTOTPDevice


class TOTPTest(TestCase):
    # The next ten tokens
    tokens = [b'179225', b'656163', b'839400', b'154567', b'346912',
              b'471576', b'45675', b'101397', b'491039', b'784503']
    secret_hex = b'2a2bbba1092ffdd25a328ad1a0a5f5d61d7aacc4'

    def setUp(self):
        """
        Create a device at the fourth time step.

        The current token is 154567.
        """
        self.factory = RequestFactory()
        try:
            self.alice = self.create_user('alice', 'password')
        except IntegrityError:  # pragma: no cover
            self.skipTest('Unable to create the test user.')
        else:
            self.device = self.alice.otoolkittotpdevice_set.create(
                secret_hex=self.secret_hex, time_step_size=30,
                start_offset=int(time() - (30 * 3)), window=0)

    def test_secret_hex(self):
        self.assertEqual(self.secret_hex, self.device.secret_hex)

    def test_secret_base32(self):
        secret_base32 = self.device.oath.base32_encode(self.device.secret,
                                                       True)
        device = OToolkitTOTPDevice.objects.create(
            user=self.alice, secret_base32=secret_base32)
        self.assertEqual(secret_base32, device.secret_base32)

    def test_secret_qrcode(self):
        request = self.factory.get('/')
        qrcode = self.device.secret_qrcode(request)
        self.assertIsInstance(qrcode, BaseImage)

    def test_single(self):
        results = [self.device.verify_token(token) for token in self.tokens]

        self.assertEqual(results, [False] * 3 + [True] + [False] * 6)

    def test_window(self):
        self.device.window = 1
        results = [self.device.verify_token(token) for token in self.tokens]

        self.assertEqual(results, [False] * 2 + [True] * 3 + [False] * 5)
