Python bindings for OATH Toolkit
================================

This package is a set of Python bindings for the `OATH Toolkit`_ library.
Please note that it is *OATH* (open authentication, e.g., one-time passwords)
and not *OAuth* (an open standard for authorization).

.. image:: https://travis-ci.org/malept/pyoath-toolkit.svg?branch=master
   :alt: Travis CI status, see https://travis-ci.org/malept/pyoath-toolkit

.. _OATH Toolkit: http://www.nongnu.org/oath-toolkit/

.. contents:: Table of Contents
   :local:

Features
--------

* Runs on a variety of Python versions/implementations
* `QR code`_ generator, compatible with apps like `Google Authenticator`_
* Integration with WTForms_
* Integration with Django via ``django-otp``

.. _Google Authenticator: https://en.wikipedia.org/wiki/Google_Authenticator
.. _QR code: https://en.wikipedia.org/wiki/QR_code
.. _WTForms: http://pypi.python.org/pypi/WTForms

Quick Install
-------------

.. note:: For a more detailed set of installation instructions, including
   optional feature prerequisites and installing from Git, please consult the
   `installation docs`_.

.. _installation docs:
   https://pyoath-toolkit.readthedocs.org/en/latest/install.html

1. Make sure CPython 2.6, 2.7, 3.3, 3.4, or PyPy ≥ 2.0 is installed.
2. Make sure `pip is installed`_.
3. Make sure ``liboath`` from `oath-toolkit is installed
   <http://nongnu.org/oath-toolkit/download.html>`_.
4. If you're using CPython, it's recommended that a C compiler and Python
   development headers/libraries are available.
5. Run the following:

   .. code-block:: shell-session

      user@host:~$ pip install pyoath-toolkit

.. _pip is installed: https://pip.pypa.io/en/latest/installing.html

Usage
-----

To generate a time-based one-time password (TOTP):

.. code-block:: python

   from oath_toolkit import TOTP
   from time import time

   digits = 6
   time_step = 30
   oath = TOTP(b'secret key', digits, time_step)
   one_time_password = oath.generate(time())

To validate a HMAC-based one-time password (HOTP):

.. code-block:: python

   from oath_toolkit import HOTP
   from oath_toolkit.exc import OATHError

   def verify(otp, counter):
       digits = 6
       oath = HOTP(b'secret key', digits)
       try:
           return oath.verify(otp, counter)
       except OATHError:
           return False

For an explanation of terms like ``time_step`` and ``counter``, refer to the
`API documentation <#documentation>`_.

More complex examples can be found in the ``examples/`` directory, which
includes a port of the command-line app ``oathtool``, a sample Django project,
and a simple Flask app which shows how WTForms integration works.

Documentation
-------------

The docs_ at `Read the Docs`_ contains information such as:

* Requirements and installation instructions
* API documentation
* Contribution guidelines and a list of contributors

.. _docs: https://pyoath-toolkit.readthedocs.org/
.. _Read the Docs: https://readthedocs.org/

License
-------

Unless otherwise noted in the respective files, the code is licensed under the
Apache License 2.0; see the ``LICENSE`` file for details on the Apache license.
The otherwise-licensed files have the requisite separate license details.
Specifically:

* ``oath_toolkit/django_otp/hotp/tests.py`` and
  ``oath_toolkit/django_otp/totp/tests.py`` are originally licensed under the
  two-clause BSD license.
* ``examples/django/example/forms.py`` is originally licensed under the MIT
  license.

The documentation is licensed under the Creative Commons
Attribution-ShareAlike 4.0 International License; see the ``LICENSE.docs``
file for details.
