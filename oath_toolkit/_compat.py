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
"""Python 2.x/3.x compatibility code."""

import itertools
import sys

try:
    unicode
except NameError:  # pragma: no cover
    unicode = None

_py2 = sys.version_info < (3,)

if _py2:  # pragma: no cover
    from urllib import quote as url_quote
    integer_types = (int, long)  # noqa
    to_bytes = \
        lambda s, e='utf-8': s.encode(e) if isinstance(s, unicode) else s
    zip_longest = itertools.izip_longest
else:  # pragma: no cover
    from urllib.parse import quote as url_quote
    integer_types = (int,)
    to_bytes = lambda s, e='utf-8': bytes(s, e) if isinstance(s, str) else s
    zip_longest = itertools.zip_longest


def bytify(chunk):
    """
    Transform a tuple chunk of bytes data from :func:`itertools.izip_longest`
    into a :func:`bytes` object.
    """
    if _py2:  # pragma: no cover
        return b''.join(chunk)
    else:  # pragma: no cover
        return bytes(chunk)

__all__ = ('bytify', 'integer_types', 'to_bytes', 'url_quote', 'zip_longest')
