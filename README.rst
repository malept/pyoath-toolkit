Python bindings for OATH Toolkit
================================

This module is a set of pure Python bindings for the `OATH Toolkit`_ library.
Please note that it is *OATH* (open authentication) and not *OAUTH* (an open
standard for authorization).

.. _OATH Toolkit: http://www.nongnu.org/oath-toolkit/

Installation
------------

This module requires the following:

* ``liboath`` is installed. If you can't find it with your distribution's
  package manager, please consult the `OATH Toolkit download page`_. This
  has been tested with 1.12.6.
* Python 2.6, 2.7, or PyPy. `According to Travis CI`_, it does not work on
  PyPy 1.9.0. I have tested it successfully on PyPy 2.0.2.
* The `CFFI`_ package.

.. _OATH Toolkit download page: http://www.nongnu.org/oath-toolkit/download.html
.. _According to Travis CI: https://travis-ci.org/malept/pyoath-toolkit/jobs/7969476
.. _CFFI: http://pypi.python.org/pypi/cffi

License
-------

Apache License 2.0: See ``LICENSE``.
