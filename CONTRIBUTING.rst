This project is hosted in two places: `GitHub`_ and `Gitorious`_. I gladly accept
pull/merge requests from both services. Gitorious does not seem to provide an
issue tracker, so the GitHub `issue tracker`_ is the only one to use at
the moment.

.. _GitHub: https://github.com/malept/pyoath-toolkit
.. _Gitorious: https://gitorious.org/pyoath-toolkit
.. _issue tracker: https://github.com/malept/pyoath-toolkit/issues

Filing Issues
-------------

Issues include bugs, feedback, and feature requests. Before you file a new
issue, please make sure that your issue has not already been filed by someone
else.

When filing a bug, please include the following information:

* Operating system name and version. If on Linux, please also include the
  distribution name.
* System architecture. For example, ``x86``, ``x86-64``, ``ARM7``.
* Python version, by running ``python -V``.
* Installed Python packages, by running ``pip freeze``.
* A detailed list of steps to reproduce the bug.
* If the bug is a Python exception, the traceback will be very helpful.

Pull Requests
-------------

If you contribute code, please also create tests for your modifications,
otherwise your request will not be accepted (I will most likely ask you to
add tests). Please make sure your pull requests pass the continuous
integration suite, by running ``tox`` before creating your submission. (Run
``pip install tox`` if it's not already installed.) The CI suite is
automatically run for every pull request on GitHub, but at this time it's
faster to run it locally. It would probably also be in your best interests to
add yourself to the ``AUTHORS.rst`` file if you have not done so already.

Development Environment
-----------------------

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
