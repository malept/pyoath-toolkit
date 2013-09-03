Python bindings for OATH Toolkit
================================

This module is a set of pure Python bindings for the `OATH Toolkit`_ library.
Please note that it is *OATH* (open authentication, e.g., one-time passwords)
and not *OAUTH* (an open standard for authorization).

.. image:: https://travis-ci.org/malept/pyoath-toolkit.png?branch=master
   :alt: Travis CI status, see https://travis-ci.org/malept/pyoath-toolkit

.. _OATH Toolkit: http://www.nongnu.org/oath-toolkit/

Installation
------------

This module requires the following:

* ``liboath`` is installed. If you can't find it with your distribution's
  package manager, please consult the `OATH Toolkit download page`_. This
  has been tested with 1.12.6.
* Python 2.6, 2.7, 3.3, or PyPy. `According to Travis CI`_, it does not work on
  PyPy 1.9.0. I have tested it successfully on PyPy 2.0.2.
* The `CFFI`_ package.
* If you wish to use the ``oath_toolkit.qrcode`` module, the `Pillow`_ and
  `qrcode`_ libraries are required.
* If you wish to use the ``oath_toolkit.wtforms`` module, the `WTForms`_
  library is required.
* If you would like to build the documentation, install `Sphinx`_ and run
  ``python setup.py build_sphinx``.

.. _OATH Toolkit download page: http://www.nongnu.org/oath-toolkit/download.html
.. _According to Travis CI: https://travis-ci.org/malept/pyoath-toolkit/jobs/7969476
.. _CFFI: http://pypi.python.org/pypi/cffi
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
includes a port of ``oathtool``.

License
-------

Apache License 2.0; see the ``LICENSE`` file for details.
