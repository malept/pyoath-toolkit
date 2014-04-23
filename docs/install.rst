Requirements
============

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
.. _Sphinx: http://sphinx-doc.org/

Installation
============

Basic installation from Git::

    pip install git+https://github.com/malept/pyoath-toolkit.git#egg=pyoath-toolkit

Installation from Git with the ``qrcode`` feature::

    pip install git+https://github.com/malept/pyoath-toolkit.git#egg=pyoath-toolkit[qrcode]
