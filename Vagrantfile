# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell", path: "bootstrap-chef.sh"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1280
    v.cpus = 2
  end
end
