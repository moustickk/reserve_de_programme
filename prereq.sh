################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
#
######################################
# installation des logiciel pré-requis
######################################
#
sudo rm /var/lib/dpkg/lock
sudo apt-get update
sudo apt-get install -y libnss3
sudo apt-get install -y software-properties-common
sudo apt-get install -y dialog
sudo apt-get install -y dirmngr
sudo apt-get install -y git
#
