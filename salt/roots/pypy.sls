{% if grains['os'] == 'Ubuntu' %}
pypy.ppa:
  pkgrepo.managed:
    - humanname: PyPy PPA
    - name: deb http://ppa.launchpad.net/pypy/ppa/ubuntu precise main
    - dist: precise
    - file: /etc/apt/sources.list.d/pypy.list
    - keyid: "68854915"
    - keyserver: keyserver.ubuntu.com
    - require_in:
      pkg: pypy-dev
{% endif %}

pypy-dev:
  pkg.installed

{% set pypy3_basename = 'pypy3-2.4.0-linux64' %}

pypy3:
  archive.extracted:
    - name: /opt/
    - source: https://bitbucket.org/pypy/pypy/downloads/{{ pypy3_basename }}.tar.bz2
    - source_hash: sha256=24e680b1742af7361107876a421dd793f5ef852dd5f097546f84b1378f7f70cc
    - archive_format: tar
    - if_missing: /opt/{{ pypy3_basename }}/

/usr/local/bin/pypy3:
  file.symlink:
    - target: /opt/{{ pypy3_basename }}/bin/pypy3
