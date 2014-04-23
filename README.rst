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

Requirements
------------

The package requires the following:

* ``liboath`` from OATH Toolkit. If you can't find it with your distribution's
  package manager, please consult the `OATH Toolkit download page`_. This
  has been tested with 1.12.6 and 2.0.2.
* It is recommended that you use this package on a **64-bit architecture**.
* Python 2.6, 2.7, 3.3, 3.4, or PyPy >= 2.0.
* One of the following:

  + For CPython, a Cython_/C extension is available. In order to compile this,
    the development/header files for ``liboath`` and a C compiler are
    required. If installing from Git, Cython 0.18 or higher is also required.
  + The `CFFI`_ package (this is included with PyPy).
* For optional ``django-otp`` integration, the django-otp_ library is required.
  Additionally, the OTP models use a field that only exists in Django_ 1.6 and
  above.
* For optional QR code support, the Pillow_ and qrcode_ libraries
  are required.
* For optional WTForms integration, the WTForms_ library is required.
* If you would like to build the documentation, install Sphinx_ and run
  ``python setup.py build_sphinx``.

.. _OATH Toolkit download page: http://www.nongnu.org/oath-toolkit/download.html
.. _Cython: http://cython.org/
.. _CFFI: http://pypi.python.org/pypi/cffi
.. _django-otp: https://pypi.python.org/pypi/django-otp
.. _Django: https://www.djangoproject.com/
.. _Pillow: http://pypi.python.org/pypi/Pillow
.. _qrcode: http://pypi.python.org/pypi/qrcode
.. _WTForms: http://pypi.python.org/pypi/WTForms
.. _Sphinx: http://sphinx-doc.org/

Installation
------------

Basic installation from Git::

    pip install git+https://github.com/malept/pyoath-toolkit.git#egg=pyoath-toolkit

Installation from Git with the ``qrcode`` feature::

    pip install git+https://github.com/malept/pyoath-toolkit.git#egg=pyoath-toolkit[qrcode]

Examples
--------

.. code-block:: python

   from oath_toolkit import TOTP
   from time import time

   digits = 6
   time_step = 30
   oath = TOTP(b'secret key', digits, time_step)
   one_time_password = oath.generate(time())

More complex examples can be found in the ``examples/`` directory, which
includes a port of ``oathtool``, a sample Django project, and a simple Flask
app, which shows how WTForms integration works.

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
Attribution-ShareAlike 3.0 Unported License; see the ``LICENSE.docs``
file for details.
