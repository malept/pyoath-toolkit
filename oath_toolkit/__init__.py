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

import base64
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


class OATH(object):
    def __init__(self):
        self._impl = oath

    @property
    def library_version(self):
        """
        The version of liboath being used.

        :rtype: :func:`bytes`
        """
        return self._impl.library_version

    def check_library_version(self, version):
        """
        Determine whether the library version is greater than or equal to the
        specified version.

        :param bytes version: The dotted version number to check
        :rtype: :func:`bool`
        """
        return self._impl.check_library_version(version)

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
            return self._impl.base32_decode(data)
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
        return self._impl.hotp_generate(secret, moving_factor, digits,
                                        add_checksum, truncation_offset)

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
        return self._impl.hotp_validate(secret, start_moving_factor,
                                        window, otp)

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
        return self._impl.totp_generate(secret, now, time_step_size,
                                        time_offset, digits)

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
        return self._impl.totp_validate(secret, now, time_step_size,
                                        start_offset, window, otp)
