# vim: set ft=yaml ts=2 sts=2 sw=2 et :
oath-toolkit.ppa:
  pkgrepo.managed:
    - humanname: OATH Toolkit PPA
    - name: deb http://ppa.launchpad.net/malept/oath-toolkit/ubuntu precise main
    - dist: precise
    - file: /etc/apt/sources.list.d/oath-toolkit.list
    - keyid: D9DF6E2D
    - keyserver: keyserver.ubuntu.com
    - require_in:
      pkg: liboath-dev

liboath-dev:
  pkg.installed

git:
  pkg.installed
