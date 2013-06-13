# -*- coding: utf-8 -*-
#
# Copyright 2013 Mark Lee
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

URI = 'otpauth://{key_type}/{issuer}:{user}?secret={secret}&issuer={issuer}'


def generate(oath, key_type, key, user, issuer):
    '''
    Generates a URI suitable for Google Authenticator.
    See: https://code.google.com/p/google-authenticator/wiki/KeyUriFormat

    :param OATH oath: OATH object
    :param str key_type: the auth type, either ``totp`` or ``hotp``
    :param str key: the string used to generate the secret key
    :param str user: the username
    :param str issuer: issuer name
    :returns: a tuple of (secret, URI)
    :rtype: (:class:`str`, :class:`str`)
    '''
    secret = oath.generate_secret_key(key)
    keys = [
        'key_type',
        'issuer',
        'user',
        'secret',
    ]
    l = locals()
    params = dict([(k, url_quote(l[k]))
                   for k in keys])
    uri = URI.format(**params)
    return secret, uri
