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

from django.db.models import BigIntegerField, F
from django.utils.translation import gettext_lazy as __
from ..models import OToolkitDevice


class OToolkitHOTPDevice(OToolkitDevice):
    '''
    HOTP-based django-otp_ ``Device``, using :mod:`oath_toolkit`.

    .. _django-otp: https://pypi.python.org/pypi/django-otp

    .. attribute:: counter

        The current position of the event counter. Upon each successful token
        verification, it increments by one.

        Defaults to ``0``.

        :type: :class:`django.db.models.BigIntegerField`
    '''
    select_name = __(u'HMAC-based OTP (HOTP) generator')
    oath_type = b'hotp'

    counter = BigIntegerField(default=0)

    class Meta:
        verbose_name = u'OATH Toolkit HOTP Device'

    def verify_token(self, token):
        verified = self._do_verify_token(token, self.oath.hotp_validate,
                                         self.counter)
        if verified is not False:
            self.counter = F('counter') + verified + 1
            self.save()
            # Update the counter value in this instance
            self.counter = self.__class__.objects.get(pk=self.pk).counter
            verified = True
        return verified
