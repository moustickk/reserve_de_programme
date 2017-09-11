################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash


# EN COURS DE CONSTRUCTION

######
# Options d'installation
######
#DIALOG=${DIALOG=dialog}
fichtemp=`tempfile 2>/dev/null` || fichtemp=/tmp/test$$
trap "rm -f $fichtemp" 0 1 2 5 15

$DIALOG --backtitle "Option" \
	--title "Options" --clear \
    --checklist "Select Option" 20 61 8 \
        0 "indi full: installation complete" off\
		1 "indi: installation personnalisée" off 2> $fichtemp

valret=$?
indi_perso=0
indi_full=0

for n in $(cat $fichtemp)
do
	case $n in
	0)
		indi_full=1
		;;
	1)
		indi_perso=1
		;;
	esac
done

# Options de apt-get pour l'installation des paquets
options="-y"
#  Désinstallation de xfce et installation de Mate
if [[ $indi_full == 1 ]]
then
    sudo apt-get install -y indi-full
fi
if [[ $indi_perso == 1 ]]
then

fi


