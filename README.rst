Python bindings for OATH Toolkit
================================

This module is a set of pure Python bindings for the `OATH Toolkit`_ library.
Please note that it is *OATH* (open authentication, e.g., one-time passwords)
and not *OAUTH* (an open standard for authorization).

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
  `qrcode`_ libraries are required. Please note that ``qrcode`` does not
  currently work on Python 3.3.
* If you would like to build the documentation, install `Sphinx`_ and run
  ``python setup.py build_sphinx``.

.. _OATH Toolkit download page: http://www.nongnu.org/oath-toolkit/download.html
.. _According to Travis CI: https://travis-ci.org/malept/pyoath-toolkit/jobs/7969476
.. _CFFI: http://pypi.python.org/pypi/cffi
.. _Pillow: http://pypi.python.org/pypi/Pillow
.. _qrcode: http://pypi.python.org/pypi/qrcode
.. _Sphinx: http://sphinx-doc.org/

License
-------

Apache License 2.0; see the ``LICENSE`` file for details.

Contributing
------------

This project is hosted in two places: `GitHub`_ and `Gitorious`_. I accept
pull/merge requests from both services. If you contribute code, please also
create tests for your modifications, otherwise your request will not be
accepted (I will most likely ask you to add tests). It would probably also
be in your best interests to add yourself to the ``CONTRIBUTORS.rst`` file
if you have not done so already.

Gitorious does not seem to provide an issue tracker, so the GitHub `issue
tracker`_ is the only one to use at the moment.

.. _GitHub: https://github.com/malept/pyoath-toolkit
.. _Gitorious: https://gitorious.org/pyoath-toolkit
.. _issue tracker: https://github.com/malept/pyoath-toolkit/issues

Build Status (master)
---------------------

.. image:: https://travis-ci.org/malept/pyoath-toolkit.png?branch=master
   :alt: Travis CI status, see https://travis-ci.org/malept/pyoath-toolkit
