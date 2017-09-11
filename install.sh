################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
#
###############################
# mise en mémoire des variables
###############################
#
dirinstall=${PWD}
cd $dirinstall
chmod +x ./*            # rendre executable les fichiers

./prereq.sh
./install_server.sh

exit
