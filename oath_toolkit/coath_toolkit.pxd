# -*- coding: utf-8 -*-

cdef extern from 'liboath/oath.h':
    ctypedef unsigned long time_t
    ctypedef unsigned long uint64_t
    ctypedef bint bool
    cdef enum:
        OATH_VERSION_NUMBER
        OATH_TOTP_DEFAULT_TIME_STEP_SIZE = 30
    #DEF VERSION_NUMBER = OATH_VERSION_NUMBER

    ctypedef enum oath_rc:
        OATH_OK = 0
        OATH_CRYPTO_ERROR = -1
        OATH_INVALID_DIGITS = -2
        OATH_PRINTF_ERROR = -3
        OATH_INVALID_HEX = -4
        OATH_TOO_SMALL_BUFFER = -5
        OATH_INVALID_OTP = -6
        OATH_REPLAYED_OTP = -7
        OATH_BAD_PASSWORD = -8
        OATH_INVALID_COUNTER = -9
        OATH_INVALID_TIMESTAMP = -10
        OATH_NO_SUCH_FILE = -11
        OATH_UNKNOWN_USER = -12
        OATH_FILE_SEEK_ERROR = -13
        OATH_FILE_CREATE_ERROR = -14
        OATH_FILE_LOCK_ERROR = -15
        OATH_FILE_RENAME_ERROR = -16
        OATH_FILE_UNLINK_ERROR = -17
        OATH_TIME_ERROR = -18
        OATH_STRCMP_ERROR = -19
        OATH_INVALID_BASE32 = -20
        OATH_BASE32_OVERFLOW = -21
        OATH_MALLOC_ERROR = -22
        OATH_FILE_FLUSH_ERROR = -23
        OATH_FILE_SYNC_ERROR = -24
        OATH_FILE_CLOSE_ERROR = -25
        OATH_LAST_ERROR = -25

    oath_rc oath_init()
    oath_rc oath_done()

    const char *oath_check_version(const char *req_version)
    const char *oath_strerror (int err)

    int oath_hotp_generate(const char *secret,
                           size_t secret_length,
                           uint64_t moving_factor,
                           unsigned digits,
                           bool add_checksum,
                           size_t truncation_offset,
                           char *output_otp)
    int oath_hotp_validate(const char *secret,
                           size_t secret_length,
                           uint64_t start_moving_factor,
                           size_t window, const char *otp)

    int oath_totp_generate(const char *secret,
                           size_t secret_length,
                           time_t now,
                           unsigned time_step_size,
                           time_t start_offset,
                           unsigned digits,
                           char *output_otp)
    int oath_totp_validate2(const char *secret,
                            size_t secret_length,
                            time_t now,
                            unsigned time_step_size,
                            time_t start_offset,
                            size_t window,
                            int *otp_pos,
                            const char *otp)

    int oath_base32_decode(const char *in_, size_t inlen,
                           char **out, size_t *outlen)
