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

from django.db.models import BigIntegerField, PositiveSmallIntegerField
from django.utils.translation import gettext_lazy as __
from time import time
from ..models import OToolkitDevice


class OToolkitTOTPDevice(OToolkitDevice):

    """
    TOTP-based django-otp_ ``Device``, using :mod:`oath_toolkit`.

    .. _django-otp: https://pypi.python.org/pypi/django-otp

    .. attribute:: time_step_size

        The time step, in seconds. In
        :class:`django_otp.plugins.otp_totp.models.TOTPDevice`, this field is
        named ``step``.

        Defaults to 30.

        :type: :class:`django.db.models.PositiveSmallIntegerField`

    .. attribute:: start_offset

        The UNIX timestamp of when to start counting time steps. In
        :class:`django_otp.plugins.otp_totp.models.TOTPDevice`, this field is
        named ``t0``.

        Defaults to ``0``.

        :type: :class:`django.db.models.BigIntegerField`
    """

    select_name = __(u'Time-based OTP (TOTP) generator')
    oath_type = b'totp'

    time_step_size = PositiveSmallIntegerField(default=30)
    start_offset = BigIntegerField(default=0)

    class Meta:
        verbose_name = u'OATH Toolkit TOTP Device'

    def verify_token(self, token):
        verified = self._do_verify_token(token, self.oath.totp_validate,
                                         time(), self.time_step_size,
                                         self.start_offset)
        if verified is not False:
            verified = True
        return verified
