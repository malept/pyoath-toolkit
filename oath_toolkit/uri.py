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

from ._compat import url_quote
from base64 import b32encode

URI = 'otpauth://{key_type}/{issuer}:{user}?secret={secret}&issuer={issuer}'


def generate(key_type, key, user, issuer, counter=None):
    """
    Generate a URI suitable for Google Authenticator.
    See: https://code.google.com/p/google-authenticator/wiki/KeyUriFormat

    :param str key_type: the auth type, either ``totp`` or ``hotp``
    :param str key: the secret key
    :param str user: the username
    :param str issuer: issuer name
    :param counter: initial counter value (HOTP only)
    :type counter: :func:`int` or :data:`None`
    :returns: a URI
    :rtype: :func:`str`
    """
    if key_type == 'hotp' and counter is None:
        raise ValueError('Using the key_type "hotp" requires a counter')
    secret = b32encode(key)
    keys = [
        'key_type',
        'issuer',
        'user',
        'secret',
    ]
    tpl = str(URI)
    if counter is not None:
        counter = str(counter)
        keys.append('counter')
        tpl += '&counter={counter}'
    l = locals()
    params = dict([(k, url_quote(l[k]))
                   for k in keys])
    return tpl.format(**params)
