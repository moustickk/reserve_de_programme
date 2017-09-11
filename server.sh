################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash


EN COURS DE CONSTRUCTION

######
# Options d'installation
######
DIALOG=${DIALOG=dialog}
fichtemp=`tempfile 2>/dev/null` || fichtemp=/tmp/test$$
trap "rm -f $fichtemp" 0 1 2 5 15
$DIALOG --backtitle "Option" \
	--title "Options" --clear \
    --checklist "Select Option" 20 61 8 \
        0 "Mate destktop and components" off\
		1 "Fr language" off 2> $fichtemp
valret=$?
language=0
installMate=0
for n in $(cat $fichtemp)
do
	case $n in
	0)
		installMate=1
		;;
	1)
		language=1
		;;
	esac
done
	
# Options de apt-get pour l'installation des paquets
options="-y"
#  Désinstallation de xfce et installation de Mate
if [[ $installMate == 1 ]]
then

fi
if [[ $language == 1 ]]
then
	
fi
