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
astroindi=/$HOME/astro-indi
#
################################################################
# copie du contenu du dossier GitHub dans /home/$USER/astro-indi
################################################################
#
cp -r $dirinstall/* $astroindi/
cd $astroindi/
chmod +x ./*            # rendre executable les fichiers


