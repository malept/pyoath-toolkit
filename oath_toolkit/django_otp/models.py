# -*- coding: utf-8 -*-
#
# Copyright 2014 Mark Lee
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

from binascii import hexlify, unhexlify
from django.contrib.sites.models import get_current_site
from django.db.models import BinaryField, PositiveSmallIntegerField
from django_otp.models import Device
from oath_toolkit import OATH, qrcode
from oath_toolkit._compat import to_bytes
from oath_toolkit.exc import OATHError
from random import SystemRandom

ASCII_MIN = 0
ASCII_MAX = 127
SECRET_SIZE = 40
rand = SystemRandom()


def _random_data():
    return b''.join([to_bytes(chr(rand.randint(ASCII_MIN, ASCII_MAX)), 'ascii')
                    for _ in range(SECRET_SIZE)])


class OToolkitDevice(Device):
    '''
    Abstract model for a :mod:`oath_toolkit`-based django-otp_ ``Device``.

    .. _django-otp: https://pypi.python.org/pypi/django-otp

    .. attribute:: secret

        Binary-encoded secret data. In
        :class:`django_otp.plugins.otp_totp.models.TOTPDevice`, this field is
        named ``key``, but this is a suboptimal choice, as ``key`` is a
        SQL keyword.

        Defaults to 40 random bytes.

        :type: :class:`django.db.models.BinaryField`

    .. attribute:: window

        The number of OTPs before and after the start OTP to test. In
        :class:`django_otp.plugins.otp_totp.models.TOTPDevice`, this field is
        named ``tolerance``.


        Defaults to ``1``.

        :type: :class:`django.db.models.PositiveSmallIntegerField`

    .. attribute:: digits

        The number of digits in the token.

        Defaults to ``6``.

        :type: :class:`django.db.models.PositiveSmallIntegerField`
    '''

    secret = BinaryField(max_length=SECRET_SIZE, default=_random_data)
    window = PositiveSmallIntegerField(default=1)
    digits = PositiveSmallIntegerField(default=6, choices=[(6, 6), (8, 8)])

    class Meta:
        abstract = True

    def secret_qrcode(self, request):
        '''
        QR code image based on the secret.

        :rtype: :class:`qrcode.image.base.BaseImage`
        '''
        site = get_current_site(request)
        return qrcode.generate(self.oath_type, self.secret,
                               self.user.username, site.name,
                               border=2, box_size=4)

    @property
    def secret_base32(self):
        '''
        The secret, in a human-readable Base32-encoded string.

        :type: bytes
        '''
        return self.oath.base32_encode(self.secret, human_readable=True)

    @secret_base32.setter
    def secret_base32(self, value):
        self.secret = self.oath.base32_decode(value)

    @property
    def secret_hex(self):
        '''
        The secret, in a hex-encoded string.

        :type: bytes
        '''
        return hexlify(self.secret)

    @secret_hex.setter
    def secret_hex(self, value):
        self.secret = unhexlify(value)

    @property
    def oath(self):
        if not hasattr(self, '_oath'):
            self._oath = OATH()
        return self._oath

    def _do_verify_token(self, token, validator_func, *args):
        token = bytes(token)
        if len(token) != self.digits:
            token = token.rjust(self.digits, b'0')
        args += (self.window, token)
        try:
            return validator_func(bytes(self.secret), *args)
        except OATHError:
            return False
