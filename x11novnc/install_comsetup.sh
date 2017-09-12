################################################
# Under GPL license
#     https://www.gnu.org/licenses/gpl.html
# Authors:	Patrick Dutoit
# 			Laurent Roge
# On June 10 2017
# V0.1
################################################
#!/bin/bash
######
# Recherche du répertoire ConfigTinker
######
dirinstall=$(find ~ -name ConfigTinker)
######
# recupere le user
######
moi=$(whoami)
data=$dirinstall

######
# Installation x11vnc
######
sudo apt -y install x11vnc
mkdir -p ~/.x11vnc
mkdir -p ~/bin/
cp $dirinstall/startx11vnc.sh ~/bin/
chmod +x ~/bin/startx11vnc.sh
~/bin/startx11vnc.sh
mkdir -p ~/.config/autostart/
cp $dirinstall/startx11vnc.desktop ~/.config/autostart/
######
# Installation accès vnc via navigateur
######
sudo apt-get install -y novnc

cd /home/$moi

git clone git://github.com/kanaka/noVNC

cat $data/novnc.service | sed -e "s/MOI/${moi}/g" > /tmp/novnc.service
sudo cp /tmp/novnc.service /etc/systemd/system/novnc.service

sudo systemctl daemon-reload
sudo systemctl enable novnc.service
sudo systemctl start novnc.service


