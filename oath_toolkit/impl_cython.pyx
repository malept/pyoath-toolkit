# -*- coding: utf-8 -*-

cimport coath_toolkit as c
from libc cimport stdlib

cdef class OATHImpl:
    def __cinit__(self):
        c.oath_init()

    def __dealloc__(self):
        c.oath_done()

    property library_version:
        '''The version of liboath being used.'''

        def __get__(self):
            return c.oath_check_version('0')

    def check_library_version(self, version):
        #cdef const char* result
        #result = c.oath_check_version(version)
        #return NULL != result
        result = c.oath_check_version(version)
        return NULL != <const char*>result


    def base32_decode(self, data):
        '''
        Decodes Base32 data. Unlike :func:`base64.b32decode`, it handles
        human-readable Base32 strings. Requires liboath 2.0.

        :param bytes data: The data to be decoded.
        :rtype: bytes
        '''
        cdef char* output = NULL
        cdef size_t output_len = 0
        cdef bytes py_string
        self._handle_retval(c.oath_base32_decode(<bytes>data, len(data),
                                                 &output, &output_len))
        try:
            py_string = <bytes>output[:output_len]
        finally:
            stdlib.free(output)
        return py_string

    def hotp_generate(self, secret, moving_factor, digits, add_checksum=False,
                      truncation_offset=None):
        '''
        Generates a one-time password using the HOTP algorithm (:rfc:`4226`).

        :param bytes secret: The secret string used to generate the one-time
                             password.
        :param int moving_factor: unsigned, can be :func:`long`, in theory.
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
        '''
        # TODO check to see if this leaks memory
        cdef char* generated = ''
        if truncation_offset is None:
            truncation_offset = (2 ** 32) - 1
        secret = <bytes>secret
        retval = c.oath_hotp_generate(secret, len(secret), moving_factor,
                                      digits, add_checksum,
                                      truncation_offset, generated)
        self._handle_retval(retval)
        return <bytes>generated

    def hotp_validate(self, secret, start_moving_factor, window, otp):
        '''
        Validates a one-time password generated using the HOTP algorithm
        (:rfc:`4226`).

        :param bytes secret: The secret used to generate the one-time password.
        :param int start_moving_factor: unsigned, can be :func:`long`, in
                                        theory. The start counter in the
                                        OTP stream.
        :param int window: The number of OTPs after the start offset OTP
                           to test.
        :param bytes otp: The one-time password to validate.
        :return: The position in the OTP window, where ``0`` is the first
                 position.
        :rtype: int
        :raise: :class:`RuntimeError` if invalid
        '''
        retval = c.oath_hotp_validate(secret, len(secret),
                                      start_moving_factor, window, otp)
        self._handle_retval(retval, True)
        return retval

    def totp_generate(self, secret, now, time_step_size, time_offset, digits):
        '''
        Generates a one-time password using the TOTP algorithm (:rfc:`6238`).

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
        '''
        # TODO check to see if this leaks memory
        cdef char* generated = ''
        if time_step_size is None:
            time_step_size = c.OATH_TOTP_DEFAULT_TIME_STEP_SIZE
        secret = <bytes>secret
        retval = c.oath_totp_generate(secret, len(secret), <int>now,
                                      time_step_size, time_offset, digits,
                                      generated)
        self._handle_retval(retval)
        return <bytes>generated

    def totp_validate(self, secret, now, time_step_size, start_offset, window,
                      otp, otp_pos=None):
        '''
        Validates a one-time password generated using the TOTP algorithm
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
        :param otp_pos: The output search position in search window
                        (defaults to :data:`None`).
        :type otp_pos: :func:`int` or :data:`None`
        :return: :data:`True` if valid
        :raise: :class:`RuntimeError` if invalid
        '''
        cdef int otp_pos_
        cdef int* c_otp_pos
        if time_step_size is None:
            time_step_size = c.OATH_TOTP_DEFAULT_TIME_STEP_SIZE
        if otp_pos is None:
            c_otp_pos = NULL
        else:
            c_otp_pos = &otp_pos_
        retval = c.oath_totp_validate2(secret, len(secret), <int>now,
                                       time_step_size, start_offset,
                                       window, c_otp_pos, otp)
        if otp_pos is not None:
            otp_pos = otp_pos_
        self._handle_retval(retval, True)
        return True

    def _handle_retval(self, retval, positive_ok=False):
        '''
        Handles the ``oath_rc`` return value from a ``liboath`` function call.

        :type retval: int
        :param bool positive_ok: Whether positive integers are acceptable (as
                                 is the case in validation functions), or throw
                                 exceptions.
        :raises: :class:`RuntimeError` containing error message on non-OK
                 return value.
        '''
        if retval != c.OATH_OK and (not positive_ok or retval < 0):
            err_str = c.oath_strerror(retval)
            err = RuntimeError(err_str)
            err.code = retval
            raise err

oath = OATHImpl()
