########################################################
# installation d'un serveur x11vnc avec démarrage auto #
########################################################
#!/bin/bash
###########
#
moi=$USER
sudo apt-get -y install x11vnc
#
echo "choisissez un mot de passe pour l'acces à distance"
read password
#
sudo x11vnc -storepasswd "$password" /home/$moi/.vnc_passwd
#
###########################
# Installation du service #
###########################
#
sudo echo -e    '[UNIT]\n
                Description=x11vnc server\n
                ConditionPathExists=/usr/bin/x11vnc\n
                \n
                [Service]\n
                Type=forking\n
                ExecStart=/bin/sh -c 'sleep 10 ; x11vnc -many -rfbauth /home/$moi/.vnc_passwd -xkb -shared -bg &'\n
                TimeoutSec=0\n
                StandardOutput=tty\n
                RemainAfterExit=yes\n
                SysVStartPriority=99\n
                \n
                [Install]\n
                WantedBy=multi-user.target' >> /tmp/x11vncserver.service

sudo cp /tmp/x11vncserver.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/x11vncserver.service
#
#################################
# enregistrer/lancer le service #
#################################
#
sudo systemctl daemon-reload
sudo systemctl enable x11vncserver.service
sudo systemctl start x11vncserver

rm /tmp/x11vncserver.service
#
exit
