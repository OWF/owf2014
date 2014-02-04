# -*- mode: ruby -*-
# vi: set ft=ruby :

python_version = "python2.7"

Vagrant.configure("2") do |config|
  config.vm.define :box do |server|
    server.ssh.username = "vagrant"

    server.vm.box = "precise64"
    server.vm.box_url = "http://files.vagrantup.com/precise64.box"
    server.vm.host_name = "owf2014"
    server.vm.network :forwarded_port, guest: 80, host: 8080, auto_correct: true
    server.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct: true
    server.vm.network :private_network, ip: "192.168.100.2"

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "deployment/server.yml"
    end
  end
end
