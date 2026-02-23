Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/jammy64"

    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.boot_timeout = 300

    config.vm.provider "virtualbox" do |vb|
        vb.memory = 2048
        vb.cpus = 2
        vb.customize ["modifyvm", :id, "--nested-hw-virt", "on"]
    end

    config.vm.provision "shell", path: "scripts/setup.sh"
end