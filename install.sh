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

chmod +x ./*.sh            # rendre executable les fichiers

./prereq.sh
./server.sh

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
    	./kstars.sh
fi
if [[ $phd2 == 1 ]]
then
	./phd2.sh
fi

DIALOG=${DIALOG=dialog}
fichtemp=`tempfile 2>/dev/null` || fichtemp=/tmp/test$$
trap "rm -f $fichtemp" 0 1 2 5 15

$DIALOG --backtitle "Option" \
	--title "Options" --clear \
    --checklist "Select Option" 0 0 0 \
        0 "installer indiwebmanager" off 2> $fichtemp

valret=$?
indiweb=0

for n in $(cat $fichtemp)
do
	case $n in
	0)
		indiweb=1
		;;
	esac
done

if [[ $indiweb == 1 ]]
then
    	./indiweb.sh
fi

exit
