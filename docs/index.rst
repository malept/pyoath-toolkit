Python bindings for OATH Toolkit
================================

This package is a set of Python bindings for the `OATH Toolkit`_ library.
Please note that it is *OATH* (open authentication, e.g., one-time passwords)
and not *OAuth* (an open standard for authorization).

.. image:: https://travis-ci.org/malept/pyoath-toolkit.svg?branch=master
   :alt: Travis CI status, see https://travis-ci.org/malept/pyoath-toolkit

.. _OATH Toolkit: http://www.nongnu.org/oath-toolkit/

Features
--------

* Runs on a variety of Python versions/implementations
* `QR code`_ generator, compatible with apps like `Google Authenticator`_
* Integration with WTForms_
* Integration with Django via ``django-otp``

.. _Google Authenticator: https://en.wikipedia.org/wiki/Google_Authenticator
.. _QR code: https://en.wikipedia.org/wiki/QR_code
.. _WTForms: http://pypi.python.org/pypi/WTForms

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
:doc:`API documentation <oath_toolkit>`.

More complex examples can be found in the ``examples/`` directory, which
includes a port of ``oathtool``, a sample Django project, and a simple Flask
app, which shows how WTForms integration works.


Table of Contents
-----------------

.. toctree::
   :maxdepth: 4

   install
   oath_toolkit
   contributing

License
-------

Unless otherwise noted in the respective files, the code is licensed under the
`Apache License 2.0`_.
The otherwise-licensed files have the requisite separate license details.
Specifically:

* ``oath_toolkit/django_otp/hotp/tests.py`` and
  ``oath_toolkit/django_otp/totp/tests.py`` are originally licensed under the
  two-clause BSD license.
* ``examples/django/example/forms.py`` is originally licensed under the MIT
  license.

The documentation is licensed under the `Creative Commons
Attribution-ShareAlike 3.0 Unported License`_.

.. _Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
.. _Creative Commons Attribution-ShareAlike 3.0 Unported License: https://creativecommons.org/licenses/by-sa/3.0/

.. ifconfig:: builder == 'html'

    Indices and tables
    ==================

    + :ref:`genindex`
    + :ref:`modindex`
    + :ref:`search`
