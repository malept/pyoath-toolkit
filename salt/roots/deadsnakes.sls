deadsnakes.ppa:
  pkgrepo.managed:
    - humanname: PyPy PPA
    - name: deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu precise main
    - dist: precise
    - file: /etc/apt/sources.list.d/deadsnakes.list
    - keyid: DB82666C
    - keyserver: keyserver.ubuntu.com
    - require_in:
      pkg:
        - python2.6-dev
        - python3.3-dev

python2.6-dev:
  pkg.installed

python3.3-dev:
  pkg.installed
