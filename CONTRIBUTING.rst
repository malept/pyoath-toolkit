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

A Vagrant_ environment is available for developing ``pyoath-toolkit``. Run
the following command in the top-level source directory (once Vagrant
is installed):

.. code-block:: shell-session

    $ vagrant up

...and it will install all of the Python dependencies in a virtualenv_. You
can then log into the virtual machine and install the package in develop mode:

.. code-block:: shell-session

    user@host:gmusicprocurator$ vagrant ssh
    # ...
    vagrant@vagrant:~$ source .virtualenv/bin/activate
    (.virtualenv)vagrant@vagrant:~$ pip install -e /vagrant

.. _Vagrant: https://www.vagrantup.com
.. _virtualenv: http://virtualenv.org/
