# vim: set ft=ruby ts=2 sts=2 sw=2 :

# 1.3.0 required for salt provisioning
# 1.5.0 required for short box names
Vagrant.require_version '>= 1.5.0'

Vagrant.configure("2") do |config|
  # using Ubuntu Precise (64-bit) because Travis CI uses it
  config.vm.box = 'hashicorp/precise64'

  config.vm.synced_folder "salt/roots/", "/srv/salt/"

  config.vm.provision :salt do |salt|
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
  end
end
