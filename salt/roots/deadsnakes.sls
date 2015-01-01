{% if grains['os'] == 'Ubuntu' %}
deadsnakes.ppa:
  pkgrepo.managed:
    - humanname: Deadsnakes PPA
    - name: deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu precise main
    - dist: precise
    - file: /etc/apt/sources.list.d/deadsnakes.list
    - keyid: DB82666C
    - keyserver: keyserver.ubuntu.com
    - require_in:
      pkg:
        - python2.6-dev
        - python3.3-dev
        - python3.4-dev
{% endif %}

python2.6-dev:
  pkg.installed

python3.3-dev:
  pkg.installed

python3.4-dev:
  pkg.installed
