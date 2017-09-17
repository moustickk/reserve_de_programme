################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
#
sudo apt-get update
chmod +x ./*.sh            # rendre executable les fichiers *.sh
chmod +x ./sous-programme/*.sh
chmod +x ./x11novnc/*.sh
#
##############################
# installation des prèrequis #
##############################
#
sudo apt-add-repository -y ppa:mutlaqja/ppa
sudo apt-add-repository -y ppa:pch/phd2 
sudo apt-get update
sudo apt-get install -y libnss3 software-properties-common dialog dirmngr git
#sudo apt-get -y purge thunderbird transmission-gtk thunar chromium-browser
#sudo apt-get -y remove --purge libreoffice*
#
#####################################
# lancer l'installation des drivers #
#####################################
#
./sous-programme/server.sh
#
###########################################################################
# installation d'Astrometry.net avec index pour la réduction astro locale #
###########################################################################
#
./sous-programme/astrometry.sh
#
##################################
# installation d'indiweb manager #
##################################
#
./sous-programme/indiweb.sh
#
##############################################################
# boite de dialogue pour les options installation prog tiers #
##############################################################
#
DIALOG=${DIALOG=dialog}
fichtemp=`tempfile 2>/dev/null` || fichtemp=/tmp/test$$
trap "rm -f $fichtemp" 0 1 2 5 15

$DIALOG --backtitle "Option" \
	--title "Options" --clear \
    --checklist "Select Option" 0 0 0 \
        0 "installer kstars" off\
		1 "installer phd2" off 2> $fichtemp

valret=$?
kstars=0
phd2=0

for n in $(cat $fichtemp)
do
	case $n in
	0)
		kstars=1
		;;
	1)
		phd2=1
		;;
	esac
done

if [[ $kstars == 1 ]]
then
    	./sous-programme/kstars.sh   # installation de kstars
fi
if [[ $phd2 == 1 ]]
then
	./sous-programme/phd2.sh     # installation de phd2
fi
#
#####################################
# instalation des communication web #
#####################################
#
./x11novnc/install_comsetup.sh
#
###########################
# fin du script principal #
###########################
#
exit
