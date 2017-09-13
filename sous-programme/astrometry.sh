################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
# script appelé par server.sh
################################################
#!/bin/bash
#
##########################################################################
# installation de astrometry.net et des index pour la réduction en local #
##########################################################################
#
sudo apt-get install -y astrometry.net
#
./sous-programme/index.sh
#
########################
# fin de script second #
########################
#
exit
