This project is hosted in two places: `GitHub`_ and `Gitorious`_. I accept
pull/merge requests from both services. If you contribute code, please also
create tests for your modifications, otherwise your request will not be
accepted (I will most likely ask you to add tests). It would probably also
be in your best interests to add yourself to the ``AUTHORS.rst`` file
if you have not done so already.

Gitorious does not seem to provide an issue tracker, so the GitHub `issue
tracker`_ is the only one to use at the moment.

.. _GitHub: https://github.com/malept/pyoath-toolkit
.. _Gitorious: https://gitorious.org/pyoath-toolkit
.. _issue tracker: https://github.com/malept/pyoath-toolkit/issues

A Vagrant_ environment is available for developing pyoath-toolkit. Simply run
the following command (once Vagrant is installed)::

    $ vagrant up

...and it will install all of the Python dependencies in a virtualenv_. You can
then log into the virtual machine::

    $ vagrant ssh
    vagrant@vagrant $ source .virtualenv/bin/activate
    vagrant@vagrant $ git clone /vagrant ~/pyoath-toolkit

The last line exists so that it is possible to run ``python setup.py sdist`` -
VirtualBox's remote filesystem module does not support hardlinks, so it fails
if you try to run that command or ``tox`` from the ``/vagrant`` directory.

.. _Vagrant: https://www.vagrantup.com
.. _virtualenv: http://virtualenv.org/
