################################################
# Under GPL license
#     https://www.gnu.org/licenses/gpl.html
# Authors:	Patrick Dutoit
# 			Laurent Roge
# On June 10 2017
# V0.1
################################################
#!/bin/bash
#
########################################
# Recherche du répertoire ConfigTinker #
########################################
#
dirinstall=$(find ~ -name x11novnc)
#
####################
# recupere le user #
####################
#
moi=$(whoami)
data=$dirinstall
#
#######################
# Installation x11vnc #
#######################
#
sudo apt -y install x11vnc
mkdir -p ~/.x11vnc
mkdir -p ~/bin/
cp $dirinstall/startx11vnc.sh ~/bin/
chmod +x ~/bin/startx11vnc.sh
~/bin/startx11vnc.sh
mkdir -p ~/.config/autostart/
cat $dirinstall/startx11vnc.desktop | sed -e "s/test/${moi}/g" > /tmp/startx11vnc.desktop
cp /tmp/startx11vnc.desktop ~/.config/autostart/
#
#########################################
# Installation accès vnc via navigateur #
#########################################
#
sudo apt-get install -y novnc
sudo apt-get install -y git

cd /home/$moi
#
#test si le dossier noVNC existe, si oui suppression
#
if [ -d "/home/${moi}/noVNC" ]
  then
  echo "suppression de l'ancien dossier noVNC"
  rm -Rf /home/$moi/noVNC
fi

git clone git://github.com/kanaka/noVNC

if [ -f /etc/systemd/system/novnc.service ]
  then
  sudo systemctl stop novnc.service
  sudo systemctl disable novnc.service
  sudo rm /etc/systemd/system/novnc.service
fi

cat $data/novnc.service | sed -e "s/MOI/${moi}/g" > /tmp/novnc.service
sudo cp /tmp/novnc.service /etc/systemd/system/novnc.service
sudo chmod 644 /etc/systemd/system/novnc.service

sudo systemctl daemon-reload
sudo systemctl enable novnc.service
sudo systemctl start novnc.service
#
#################
# fin du script #
#################
#
