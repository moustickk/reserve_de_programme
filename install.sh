################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
#
# récuperer le chemin des script
#
workFolder=$(readlink -f $(dirname $0))
#
time=2    #temps de pause avant une étape d'installation
#
sudo apt-get update
chmod +x ./*.sh            # rendre executable les fichiers *.sh
chmod +x ./sous-programme/*.sh
chmod +x ./x11novnc/*.sh
#
##############################
# installation des prérequis #
##############################
echo "########################## installation des prérequis ##########################"
sleep $time
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
echo "########################## installation des drivers indi ##########################"
sleep $time
#
./sous-programme/server.sh workFolder
#
###########################################################################
# installation d'Astrometry.net avec index pour la réduction astro locale #
###########################################################################
echo "########################## installation d'Astrometry.net et index ##########################"
sleep $time
#
./sous-programme/astrometry.sh workFolder
#
##################################
# installation d'indiweb manager #
##################################
echo "########################## installation d'IndiWeb Manager ##########################"
sleep $time
#
./sous-programme/indiweb.sh workFolder
#
#####################################
# instalation des communication web #
#####################################
echo "########################## installation de x11 et noVNC ##########################"
sleep $time
#
./x11novnc/install_comsetup.sh workFolder
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
	echo "########################## installation de Kstars ##########################"
	sleep $time
    	./sous-programme/kstars.sh workFolder   # installation de kstars
fi
if [[ $phd2 == 1 ]]
then
	echo "########################## installation de phd2 ##########################"
	sleep $time
	./sous-programme/phd2.sh workFolder     # installation de phd2
fi
# 
###########################
# création des raccourcis #
###########################
#
echo "########################## création des raccourcis ##########################"
sleep $time
#
./sous-programme/shortcut.sh workFolder kstars
./sous-programme/shortcut.sh workFolder phd2
#
###########################
# fin du script principal #
###########################
#
whiptail --title "Fin de script" --msgbox "l'installation est finie,\n
vous avez maintenant une serveur astro près. Il y 2 connexion au serveur accessible par naviguateur sur le reseau\n
indiwebmanager accessible a l'adresse "http://ip-du-serveur:8624"\n
le bureau a distance a l'adresse "http://ip-du-serveur:5901/vnc.html"" 0 0
#
exit
