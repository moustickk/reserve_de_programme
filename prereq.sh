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
sudo apt-add-repository -y ppa:mutlaqja/ppa
sudo apt-add-repository -y ppa:pch/phd2 
sudo apt-get update
sudo apt-get install -y libnss3 software-properties-common dialog dirmngr git
#
exit
