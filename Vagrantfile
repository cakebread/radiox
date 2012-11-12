

# Copyright 2012 Rob Cakebread

Vagrant::Config.run do |config|
  config.vm.define :radioxvm do |radiox_config|

      radiox_config.vm.box = "radiox"

      #Use a 32 bit on a VPS if it has less than 4gigs RAM:
      radiox_config.vm.box_url = "http://files.vagrantup.com/precise32.box"

      #Use a 64 bit box if you have 4+ gigs ram
      #Warning, have not tested 64 bit image
      #radiox_config.vm.box_url = "http://files.vagrantup.com/precise64.box"


      ###################
      # Port forwarding ->
      ###################

      # Airtime web interface
      radiox_config.vm.forward_port 80, 9080


      # Icecast2 stream
      radiox_config.vm.forward_port 8000, 9999

  end
end


