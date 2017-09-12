################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
# script appelé par install.sh
################################################
#!/bin/bash
#
#####################################################################
# boite de dialogue pour choisir le type d'installation des drivers #
#####################################################################
#
DIALOG=${DIALOG=dialog}
fichtemp=`tempfile 2>/dev/null` || fichtemp=/tmp/test$$
trap "rm -f $fichtemp" 0 1 2 5 15

$DIALOG --backtitle "Choix installation drivers" \
	--title "choix des drivers à installer" --clear \
    --radiolist "Select Option" 0 0 0 \
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

if [[ $indi_full == 1 ]]
then
    	./sous-programme/indi-full.sh
fi
if [[ $indi_perso == 1 ]]
then
	./sous-programme/indi-perso.sh
fi
#
############################
# fin de script secondaire #
############################
#
exit
