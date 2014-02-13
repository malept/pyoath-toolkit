Python bindings for OATH Toolkit
================================

This module is a set of Python bindings for the `OATH Toolkit`_ library.
Please note that it is *OATH* (open authentication, e.g., one-time passwords)
and not *OAUTH* (an open standard for authorization).

.. image:: https://travis-ci.org/malept/pyoath-toolkit.png?branch=master
   :alt: Travis CI status, see https://travis-ci.org/malept/pyoath-toolkit

.. _OATH Toolkit: http://www.nongnu.org/oath-toolkit/

Installation
------------

This module requires the following:

* ``liboath`` from OATH Toolkit. If you can't find it with your distribution's
  package manager, please consult the `OATH Toolkit download page`_. This
  has been tested with 1.12.6.
* Python 2.6, 2.7, 3.3, or PyPy >= 2.0.
* One of the following:

  * If you are not running PyPy and installing from Git, Cython 0.18 or higher
    and a C compiler is recommended, plus the development/header files for
    ``liboath``.
  * If you are not running PyPy and installing from an officially released
    tarball, a C compiler is recommended, plus the development/header files
    for ``liboath``.
* The `CFFI`_ package (this is included with PyPy).
* For optional ``django-otp`` integration, the django-otp_ library is required.
  Additionally, the OTP models use a field that only exists in Django_ 1.6 and
  above.
* For optional `QR code`_ support, the `Pillow`_ and `qrcode`_ libraries
  are required.
* For optional WTForms integration, the `WTForms`_ library is required.
* If you would like to build the documentation, install `Sphinx`_ and run
  ``python setup.py build_sphinx``.

.. _OATH Toolkit download page: http://www.nongnu.org/oath-toolkit/download.html
.. _According to Travis CI: https://travis-ci.org/malept/pyoath-toolkit/jobs/7969476
.. _CFFI: http://pypi.python.org/pypi/cffi
.. _django-otp: https://pypi.python.org/pypi/django-otp
.. _Django: https://www.djangoproject.com/
.. _QR code: https://en.wikipedia.org/wiki/QR_code
.. _Pillow: http://pypi.python.org/pypi/Pillow
.. _qrcode: http://pypi.python.org/pypi/qrcode
.. _WTForms: http://pypi.python.org/pypi/WTForms
.. _Sphinx: http://sphinx-doc.org/

Basic installation from Git::

    pip install git+git://github.com/malept/pyoath-toolkit.git#egg=pyoath-toolkit

Installation from Git with the ``qrcode`` feature::

    pip install git+git://github.com/malept/pyoath-toolkit.git#egg=pyoath-toolkit[qrcode]

Examples
--------

.. code-block:: python

   from oath_toolkit import OATH
   from time import time

   oath = OATH()
   one_time_password = oath.totp_generate(b'hello world', time(), None, 0, 6)

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
