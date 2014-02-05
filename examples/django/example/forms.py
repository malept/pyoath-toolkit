# -*- coding: utf-8 -*-
#
# Originally from:
# * Repository: https://github.com/Bouke/django-two-factor-auth/
# * Revision: d6bd2eae
# * Path: /two_factor/forms.py
#
# Copyright (C) 2014 Bouke Haarsma, Mark Lee
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from django import forms
from django.utils.translation import ugettext_lazy as _


class DeviceValidationForm(forms.Form):
    '''Validates that a OTP device is working properly.'''
    token = forms.IntegerField(label=_(u'Token'), min_value=1,
                               max_value=999999)

    def __init__(self, device, *args, **kwargs):
        super(DeviceValidationForm, self).__init__(*args, **kwargs)
        self.device = device

    def clean_token(self):
        token = self.cleaned_data['token']
        if not self.device.verify_token(token):
            raise forms.ValidationError(_(u'Entered token is not valid'))
        return token
