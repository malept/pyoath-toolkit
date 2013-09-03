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

import sys

try:
    unicode
except NameError:
    unicode = None

if sys.version_info < (3,):  # pragma: no cover
    from urllib import quote as url_quote
    to_bytes = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s
else:  # pragma: no cover
    from urllib.parse import quote as url_quote
    to_bytes = lambda s: bytes(s, 'utf-8') if isinstance(s, str) else s

__all__ = ['to_bytes', 'url_quote']
