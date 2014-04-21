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
CFFI_-based bindings for OATH Toolkit.

Most of the docs and declarations come from the OATH Toolkit docs_.

.. _CFFI: http://cffi.readthedocs.org/
.. _docs: http://www.nongnu.org/oath-toolkit/liboath-api/liboath-oath.html
"""

from __future__ import division

from ._compat import integer_types, to_bytes
from .exc import OATHError
from .types import OTPPosition

import atexit
from cffi import FFI
import os

LIBRARY_NAME = os.environ.get('LIBOATH_NAME', 'oath')

declarations = '''
typedef _Bool bool;
/* cffi doesn't know about time_t */
typedef long time_t;

/* defines */
static char *const OATH_VERSION;
static time_t const OATH_TOTP_DEFAULT_START_TIME;
static const int OATH_TOTP_DEFAULT_TIME_STEP_SIZE;

typedef enum {
  OATH_OK = 0,
  OATH_CRYPTO_ERROR = -1,
  OATH_INVALID_DIGITS = -2,
  OATH_PRINTF_ERROR = -3,
  OATH_INVALID_HEX = -4,
  OATH_TOO_SMALL_BUFFER = -5,
  OATH_INVALID_OTP = -6,
  OATH_REPLAYED_OTP = -7,
  OATH_BAD_PASSWORD = -8,
  OATH_INVALID_COUNTER = -9,
  OATH_INVALID_TIMESTAMP = -10,
  OATH_NO_SUCH_FILE = -11,
  OATH_UNKNOWN_USER = -12,
  OATH_FILE_SEEK_ERROR = -13,
  OATH_FILE_CREATE_ERROR = -14,
  OATH_FILE_LOCK_ERROR = -15,
  OATH_FILE_RENAME_ERROR = -16,
  OATH_FILE_UNLINK_ERROR = -17,
  OATH_TIME_ERROR = -18,
  OATH_STRCMP_ERROR = -19,
  OATH_INVALID_BASE32 = -20,
  OATH_BASE32_OVERFLOW = -21,
  OATH_MALLOC_ERROR = -22,
  OATH_FILE_FLUSH_ERROR = -23,
  OATH_FILE_SYNC_ERROR = -24,
  OATH_FILE_CLOSE_ERROR = -25,
  /* When adding anything here, update OATH_LAST_ERROR, errors.c
     and tests/tst_errors.c. */
  OATH_LAST_ERROR = -25
} oath_rc;

/* from oath-toolkit */
const char * oath_strerror               (oath_rc err);
const char * oath_strerror_name          (oath_rc err);

/* for some reason, need to keep the following function in,
 * or it segfaults.
 */
oath_rc      oath_init                   (void);
oath_rc      oath_done                   (void);
const char * oath_check_version          (const char *req_version);
int          oath_base32_decode          (const char *in,
                                          size_t inlen,
                                          char **out,
                                          size_t *outlen);
oath_rc      oath_hotp_generate          (const char *secret,
                                          size_t secret_length,
                                          uint64_t moving_factor,
                                          unsigned  digits,
                                          bool add_checksum,
                                          size_t truncation_offset,
                                          char *output_otp);
oath_rc      oath_hotp_validate          (const char *secret,
                                          size_t secret_length,
                                          uint64_t start_moving_factor,
                                          size_t window,
                                          const char *otp);
oath_rc      oath_totp_generate          (const char *secret,
                                          size_t secret_length,
                                          time_t now,
                                          unsigned  time_step_size,
                                          time_t start_offset,
                                          unsigned  digits,
                                          char *output_otp);
oath_rc      oath_totp_validate2         (const char *secret,
                                          size_t secret_length,
                                          time_t now,
                                          unsigned  time_step_size,
                                          time_t start_offset,
                                          size_t window,
                                          int *otp_pos,
                                          const char *otp);
'''

_ffi = FFI()
_ffi.cdef(declarations)
c = _ffi.dlopen(LIBRARY_NAME)


def _handle_retval(retval, positive_ok=False):
    """
    Handle the ``oath_rc`` return value from a ``liboath`` function call.

    :type retval: int
    :param bool positive_ok: Whether positive integers are acceptable (as is
                             the case in validation functions), or throw
                             exceptions.
    :raises: :class:`OATHError` containing error message on non-OK
             return value.
    """
    if retval != c.OATH_OK and (not positive_ok or retval < 0):
        errno = _ffi.cast('oath_rc', retval)
        err_str = _ffi.string(c.oath_strerror(errno))
        err = OATHError(err_str)
        err.code = errno
        raise err

_handle_retval(c.oath_init())
atexit.register(c.oath_done)
library_version = _ffi.string(c.oath_check_version(b'0'))


def check_library_version(version):
    """
    Determine whether the library version is greater than or equal to the
    specified version.

    :param bytes version: The dotted version number to check
    :rtype: :func:`bool`
    """
    return c.oath_check_version(to_bytes(version)) != _ffi.NULL


def base32_decode(data):
    """
    Decode Base32 data.

    Unlike :func:`base64.b32decode`, it handles human-readable Base32 strings.
    Requires liboath 2.0.

    :param bytes data: The data to be decoded.
    :rtype: bytes
    """
    output = _ffi.new('char **')
    output_len = _ffi.new('size_t *')
    _handle_retval(c.oath_base32_decode(to_bytes(data), len(data), output,
                                        output_len))
    return _ffi.string(output[0], output_len[0])


def hotp_generate(secret, moving_factor, digits, add_checksum=False,
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
    :param bool add_checksum: Whether to add a checksum digit (depending on the
                              version of ``liboath`` used, this may be
                              ignored).
    :param truncation_offset: A truncation offset to use, if not set to
                              :data:`None`.
    :type truncation_offset: :func:`int` or :data:`None`
    :return: one-time password
    :rtype: :func:`bytes`
    """
    if truncation_offset is None:
        truncation_offset = (2 ** 32) - 1
    generated = _ffi.new('char *')
    secret = to_bytes(secret)
    retval = c.oath_hotp_generate(secret, len(secret), moving_factor, digits,
                                  add_checksum, truncation_offset, generated)
    _handle_retval(retval)
    return _ffi.string(generated, digits)


def hotp_validate(secret, start_moving_factor, window, otp):
    """
    Validate a one-time password generated using the HOTP algorithm
    (:rfc:`4226`).

    :param bytes secret: The secret used to generate the one-time password.
    :param int start_moving_factor: Unsigned, can be :func:`long`, in theory.
                                    The start counter in the OTP stream.
    :param int window: The number of OTPs after the start offset OTP
                       to test.
    :param bytes otp: The one-time password to validate.
    :return: The position in the OTP window, where ``0`` is the first position.
    :rtype: :class:`oath_toolkit.types.OTPPosition`
    :raise: :class:`OATHError` if invalid
    """
    retval = c.oath_hotp_validate(secret, len(secret), start_moving_factor,
                                  window, otp)
    _handle_retval(retval, True)
    return OTPPosition(absolute=None, relative=retval)


def totp_generate(secret, now, time_step_size, time_offset, digits):
    """
    Generate a one-time password using the TOTP algorithm (:rfc:`6238`).

    :param bytes secret: The secret string used to generate the one-time
                         password.
    :param int now: The UNIX timestamp (usually the current one)
    :param time_step_size: Unsigned, the time step system parameter. If set to
                           :data:`None`, defaults to ``30``.
    :type time_step_size: :func:`int` or :data:`None`
    :param int time_offset: The UNIX timestamp of when to start counting
                            time steps (usually should be ``0``).
    :param int digits: The number of digits of the one-time password.
    :return: one-time password
    :rtype: :func:`bytes`
    """
    if time_step_size is None:
        time_step_size = 30  # c.OATH_TOTP_DEFAULT_TIME_STEP_SIZE
    generated = _ffi.new('char *')
    secret = to_bytes(secret)
    if not isinstance(now, integer_types):
        now = int(now)
    retval = c.oath_totp_generate(secret, len(secret), now, time_step_size,
                                  time_offset, digits, generated)
    _handle_retval(retval)
    return _ffi.string(generated, digits)


def totp_validate(secret, now, time_step_size, start_offset, window, otp):
    """
    Validate a one-time password generated using the TOTP algorithm
    (:rfc:`6238`).

    :param bytes secret: The secret used to generate the one-time password.
    :param int now: The UNIX timestamp (usually the current one)
    :param time_step_size: Unsigned, the time step system parameter. If set to
                           :data:`None`, defaults to ``30``.
    :type time_step_size: :func:`int` or :data:`None`
    :param int start_offset: The UNIX timestamp of when to start counting time
                             steps (usually should be ``0``).
    :param int window: The number of OTPs before and after the start OTP
                       to test.
    :param bytes otp: The one-time password to validate.
    :return: The absolute and relative positions in the OTP window, where ``0``
             is the first position.
    :rtype: :class:`oath_toolkit.types.OTPPosition`
    :raise: :class:`OATHError` if invalid
    """
    if time_step_size is None:
        time_step_size = 30  # c.OATH_TOTP_DEFAULT_TIME_STEP_SIZE
    addr_otp_pos = _ffi.new('int *')
    if not isinstance(now, integer_types):
        now = int(now)
    retval = c.oath_totp_validate2(secret, len(secret), now, time_step_size,
                                   start_offset, window, addr_otp_pos, otp)
    _handle_retval(retval, True)
    return OTPPosition(absolute=retval, relative=addr_otp_pos[0])
