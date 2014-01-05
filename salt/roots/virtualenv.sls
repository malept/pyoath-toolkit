requirements-deps:
  pkg.installed:
    - names:
      - python-dev
      - libffi-dev

python-virtualenv:
  pkg.installed

/home/vagrant/.virtualenv:
  virtualenv.managed:
    # The following directive fixes relative dirs for requirements*.txt for some reason
    - no_chown: True
    - requirements: /vagrant/requirements-dev.txt
    - use_wheel: True
    - user: vagrant
    - requires:
      - pkg: python-virtualenv
      - pkg: requirements-deps
