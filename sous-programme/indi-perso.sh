################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
# script appelé par server.sh
################################################
#!/bin/bash
#
sudo apt-get -y install libindi1
#
#################################
# choix des drivers à installer #
#################################
#
exitstatus=0
while [ $exitstatus == 0 ]
do
Name=$(whiptail --title "choix des drivers" --inputbox "ecrire le nom de votre driver, lorsque vous avez fini faites annuler" 0 0 indi- 3>&1 1>&2 2>&3)
 
exitstatus=$?
if [ $exitstatus = 0 ]; then
    sudo apt-get -y install $Name
else
    exitstatus=1
fi
done
#
########################
# fin de script tierce #
########################
#

