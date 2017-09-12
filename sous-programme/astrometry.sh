################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
#
##########################################################################
# installation de astrometry.net et des index pour la réduction en local #
##########################################################################
#
sudo apt-get -y install astrometry.net
#
./sous-programme/index.sh
#
########################
# fin de script second #
########################
#
exit
