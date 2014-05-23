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

from __future__ import absolute_import

from . import unittest
from .._compat import to_bytes
from ..wtforms import HOTPValidator, TOTPValidator
from time import time
from wtforms import ValidationError


# from WTForms, tests/validators.py


class DummyTranslations(object):
    def gettext(self, string):
        return string


class DummyUser(object):
    oath_secret = b'\x00\x00'


class DummyForm(dict):
    user = DummyUser()


class DummyField(object):
    _translations = DummyTranslations()

    def __init__(self, data, errors=(), raw_data=None):
        self.data = data
        self.errors = list(errors)
        self.raw_data = raw_data

    def gettext(self, string):
        return self._translations.gettext(string)


class WTFormsTestCase(unittest.TestCase):

    def setUp(self):
        self.form = DummyForm()

    def test_hotp_validation(self):
        hotp_validator = HOTPValidator(6, 0, 0,
                                       get_secret=lambda fm, fd: b'\x00\x00')
        self.assert_validations(hotp_validator)

    def test_totp_validation_with_defaults(self):
        digits = 6
        totp_validator = TOTPValidator(digits, 0)
        secret = DummyUser.oath_secret
        otp = totp_validator.oath.totp_generate(secret, time(), 30, 0, digits)
        self.assert_validations(totp_validator, otp.decode('utf-8'))

    def test_totp_validation(self):
        totp_validator = TOTPValidator(6, 0, verbose_errors=True,
                                       start_time=time(),
                                       time_step_size=300)
        self.assert_validations(totp_validator)

    def validate_value(self, validator, value):
        return validator(self.form, DummyField(value))

    def assert_validation_passes(self, validator, value):
        self.assertIsNone(self.validate_value(validator, value))

    def assert_validation_fails(self, validator, value):
        with self.assertRaises(ValidationError):
            self.validate_value(validator, value)

    def assert_validations(self, validator, valid_otp=u'328482'):
        self.assert_validation_passes(validator, valid_otp)
        self.assert_validation_passes(validator, to_bytes(valid_otp))
        self.assert_validation_fails(validator, b'')
        self.assert_validation_fails(validator, b'invalid')
        self.assert_validation_fails(validator, b'hello!')
        self.assert_validation_fails(validator, b'123456')
        self.assert_validation_fails(validator, u'✓✓✓✓✓✓')
