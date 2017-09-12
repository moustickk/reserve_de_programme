################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
###########
# pre-req #
###########
#
sudo apt-get -y install python-pip
#
#######################################
# installation des sources du serveur #
#######################################
#
pip install indiweb
#
###########################
# Installation du service #
###########################
#
dir=/etc/systemd/system
MOI=$USER

sudo updatedb     # mettre à jour la base d'indexation

dirindiweb=$(locate indi-web)  #récupérer le chemin du binaire indi-web

sudo echo -e '[UNIT]\nDescription=INDI Web Manager\nAfter=multi-user.target\n\n[Service]\nType=idle\nUser='$MOI'\nExecStart='$dirindiweb' -v\nRestart=Always\nRestartSec=5\n\n[Install]\nWantedBy=multi-user.target' >> /tmp/indiwebmanager.service

sudo cp /tmp/indiwebmanager.service $dir/
sudo chmod 644 $dir/indiwebmanager.service
#
#################################
# enregistrer/lancer le service #
#################################
#
sudo systemctl daemon-reload
sudo systemctl enable indiwebmanager.service
sudo systemctl start indiwebmanager
rm /tmp/indiwebmanager.service

exit
