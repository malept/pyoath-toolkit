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
"""
Base API for handling one-time passwords.

There are two API types: simple and advanced. The simple API (:class:`HOTP`
and :class:`TOTP`) is based on the two-factor authentication API in the
`Cryptography library`_. The advanced API (:class:`OATH`) is based on the
functional API in OATH Toolkit's liboath_.

When compared to the :class:`HOTP`/:class:`TOTP` classes:

* :class:`OATH` has a more customizable set of parameters.
* :class:`OATH` is more likely to add parameters to its method as OATH Toolkit
  gains APIs.

.. _Cryptography library: https://cryptography.io/
.. _liboath: http://oath-toolkit.nongnu.org/liboath-api/liboath-oath.html
"""

from abc import ABCMeta
import base64
import hashlib
import os
if not os.environ.get('READTHEDOCS') and not os.environ.get('SETUP_PY'):
    try:  # pragma: no cover
        from . import impl_cython as oath
    except ImportError:  # pragma: no cover
        from . import impl_cffi as oath
from .exc import OATHError
from .metadata import DESCRIPTION, VERSION

__description__ = DESCRIPTION
__version__ = VERSION

OTP_ALGORITHMS = (
    hashlib.sha1,
    # hashlib.sha256,
    # hashlib.sha512,
)


class OTP(object):

    """Base class for one-time password (OTP) implementations."""

    __metaclass__ = ABCMeta
    __slots__ = ['_algorithm']

    def __init__(self, key, length, algorithm=None):
        if not algorithm:
            algorithm = hashlib.sha1
        self.algorithm = algorithm

        self.key = key
        self.length = length

    @property
    def algorithm(self):
        """
        The hash algorithm used during OTP generation.

        Not currently implemented (requires liboath >= 2.6.0).
        """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        if value not in OTP_ALGORITHMS:
            raise ValueError('Unrecognized OTP algorithm')
        self._algorithm = value


class HOTP(OTP):

    """
    HMAC-based one-time password (HOTP) convenience implementation.

    API based on :class:`cryptography.hazmat.primitives.twofactor.hotp.HOTP`.

    :param bytes key: The secret key.
    :param int length: The length of generated one-time passwords.
    :param algorithm: The hash algorithm used during OTP generation. Not
                      currently implemented (requires liboath >= 2.6.0).
                      Defaults to HMAC-SHA1.
    """

    __slots__ = ['key', 'length', '_algorithm']

    def __init__(self, key, length, algorithm=None):
        super(HOTP, self).__init__(key, length, algorithm)

    def generate(self, counter):
        """
        Generate an OTP at the specified offset in the OTP stream.

        :param counter: The start counter in the OTP stream.
        :type counter: :func:`int` or :func:`long`
        :rtype: :func:`bytes`
        """
        return oath.hotp_generate(self.key, counter, self.length)

    def verify(self, hotp, counter, window=0):
        """
        Verify that the given one-time password is within the range of
        generated OTPs, given ``counter`` and ``window``.

        :param bytes hotp: The OTP to verify.
        :param counter: The start counter in the OTP stream.
        :type counter: :func:`int` or :func:`long`
        :param int window: The number of OTPs after the start counter to test.
        :return: The position in the OTP window, where ``0`` is the first
                 position.
        :rtype: :func:`int`
        :raise: :class:`OATHError` if invalid
        """
        return oath.hotp_validate(self.key, counter, window, hotp)


class TOTP(OTP):

    """
    Time-based one-time password (TOTP) convenience implementation.

    API based on :class:`cryptography.hazmat.primitives.twofactor.totp.TOTP`.

    :param bytes key: The secret key.
    :param int length: The length of generated one-time passwords.
    :param algorithm: The hash algorithm used during OTP generation. Not
                      currently implemented (requires liboath >= 2.6.0).
                      Defaults to HMAC-SHA1.
    """

    __slots__ = ['key', 'length', '_algorithm', 'time_step']

    def __init__(self, key, length, time_step, algorithm=None):
        super(TOTP, self).__init__(key, length, algorithm)
        self.time_step = time_step

    def generate(self, time):
        """
        Generate an OTP for the given time value.

        :param time: The UNIX timestamp-encoded time value.
        :type time: :func:`int` or :func:`long`
        :rtype: :func:`bytes`
        """
        return oath.totp_generate(self.key, time, self.time_step, 0,
                                  self.length)

    def verify(self, totp, time, window=0):
        """
        Verify that the given one-time password is within the range of
        generated OTPs, given ``counter`` and ``window``.

        :param bytes totp: The OTP to verify.
        :param time: The UNIX timestamp-encoded time value.
        :type time: :func:`int` or :func:`long`
        :param int window: The number of OTPs before and after the start OTP
                           to test.
        :return: The position in the OTP window, where ``0`` is the first
                 position.
        :rtype: :func:`int`
        :raise: :class:`OATHError` if invalid
        """
        return oath.totp_validate(self.key, time, self.time_step, 0, window,
                                  totp)


class OATH(object):

    """
    A convenience class that is a direct port of the OATH Toolkit API.
    """

    __slots__ = []

    @property
    def library_version(self):
        """
        The version of liboath being used.

        :rtype: :func:`bytes`
        """
        return oath.library_version

    def check_library_version(self, version):
        """
        Determine whether the library version is greater than or equal to the
        specified version.

        :param bytes version: The dotted version number to check
        :rtype: :func:`bool`
        """
        return oath.check_library_version(version)

    @staticmethod
    def _chunk_iterable(iterable, n, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks.

        >>> list(OATH._chunk_iterable('ABCDEFG', 3, 'x'))
        ['ABC', 'DEF', 'Gxx']

        Copied from the Python documentation in the itertools module.
        """
        from ._compat import zip_longest
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    def base32_encode(self, data, human_readable=False):
        """
        Base32-encode data.

        :param data: The data to be encoded. Must be castable into a
                     :func:`bytes` object.
        :param bool human_readable: If :data:`True`, transforms the Base32
                                    string into space-separated chunks of 4
                                    characters, removing trailing ``=``.
        :rtype: bytes
        """
        from ._compat import bytify, to_bytes
        if not data:
            return b''
        encoded = base64.b32encode(to_bytes(data))
        if human_readable:
            chunked_iterable = self._chunk_iterable(encoded, 4)
            encoded = b' '.join([bytify(chunk)
                                 for chunk in chunked_iterable])
            encoded = encoded.rstrip(b'=')
        return encoded

    def _py_base32_decode(self, data):
        data = data.replace(b' ', b'').upper()
        if len(data) % 8 != 0:
            data = data.ljust((int(len(data) / 8) + 1) * 8, b'=')
        return base64.b32decode(data)

    def base32_decode(self, data):
        """
        Decode Base32 data. Unlike :func:`base64.b32decode`, it handles
        human-readable Base32 strings.

        :param bytes data: The data to be decoded.
        :rtype: bytes
        """
        if not data:
            raise OATHError('Invalid base32 string')
        elif not (data.isupper() or data.islower()):
            raise OATHError(
                'Base32 string cannot be both upper- and lowercased')
        if self.check_library_version(b'2.0.0'):  # pragma: no cover
            return oath.base32_decode(data)
        else:  # pragma: no cover
            return self._py_base32_decode(data)

    def hotp_generate(self, secret, moving_factor, digits, add_checksum=False,
                      truncation_offset=None):
        """
        Generate a one-time password using the HOTP algorithm (:rfc:`4226`).

        :param bytes secret: The secret string used to generate the one-time
                             password.
        :param int moving_factor: unsigned, can be :func:`long`, in theory. A
                                  counter indicating where in OTP stream to
                                  generate an OTP.
        :param int digits: unsigned, the number of digits of the one-time
                           password.
        :param bool add_checksum: Whether to add a checksum digit (depending
                                  on the version of ``liboath`` used, this may
                                  be ignored).
        :param truncation_offset: A truncation offset to use, if not set to
                                  :data:`None`.
        :type truncation_offset: :func:`int` or :data:`None`
        :return: one-time password
        :rtype: :func:`bytes`
        """
        return oath.hotp_generate(secret, moving_factor, digits, add_checksum,
                                  truncation_offset)

    def hotp_validate(self, secret, start_moving_factor, window, otp):
        """
        Validate a one-time password generated using the HOTP algorithm
        (:rfc:`4226`).

        :param bytes secret: The secret used to generate the one-time password.
        :param int start_moving_factor: Unsigned, can be :func:`long`, in
                                        theory. The start counter in the
                                        OTP stream.
        :param int window: The number of OTPs after the start offset OTP
                           to test.
        :param bytes otp: The one-time password to validate.
        :return: The position in the OTP window, where ``0`` is the first
                 position.
        :rtype: int
        :raise: :class:`OATHError` if invalid
        """
        return oath.hotp_validate(secret, start_moving_factor, window, otp)

    def totp_generate(self, secret, now, time_step_size, time_offset, digits):
        """
        Generate a one-time password using the TOTP algorithm (:rfc:`6238`).

        :param bytes secret: The secret string used to generate the one-time
                             password.
        :param int now: The UNIX timestamp (usually the current one)
        :param time_step_size: Unsigned, the time step system parameter. If
                               set to :data:`None`, defaults to ``30``.
        :type time_step_size: :func:`int` or :data:`None`
        :param int time_offset: The UNIX timestamp of when to start counting
                                time steps (usually should be ``0``).
        :param int digits: The number of digits of the one-time password.
        :return: one-time password
        :rtype: :func:`bytes`
        """
        return oath.totp_generate(secret, now, time_step_size, time_offset,
                                  digits)

    def totp_validate(self, secret, now, time_step_size, start_offset, window,
                      otp):
        """
        Validate a one-time password generated using the TOTP algorithm
        (:rfc:`6238`).

        :param bytes secret: The secret used to generate the one-time password.
        :param int now: The UNIX timestamp (usually the current one)
        :param time_step_size: Unsigned, the time step system parameter. If
                               set to :data:`None`, defaults to ``30``.
        :type time_step_size: :func:`int` or :data:`None`
        :param int start_offset: The UNIX timestamp of when to start counting
                                 time steps (usually should be ``0``).
        :param int window: The number of OTPs before and after the start OTP
                           to test.
        :param bytes otp: The one-time password to validate.
        :return: The absolute and relative positions in the OTP window, where
                 ``0`` is the first position.
        :rtype: :class:`oath_toolkit.types.OTPPosition`
        :raise: :class:`OATHError` if invalid
        """
        return oath.totp_validate(secret, now, time_step_size, start_offset,
                                  window, otp)
