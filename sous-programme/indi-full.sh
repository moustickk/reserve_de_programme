################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
#
########################################################
# installation de indi-full avec drivers autres (Atik) #
########################################################
#
sudo apt-get install -y indi-full
#
#########################
# detection achitecture #
#########################
#
case $(uname -p) in
"armv7l")
    proc="-armhf"
    ;;
"x86_64")
    proc="-amd64"
    ;;
esac
#
##################
# telechargement #
##################
#

software="atikccd"
version="$software""-""1.24"
file="$version""$proc.deb"
echo $file
wget http://download.cloudmakers.eu/$file -P /tmp/
sudo dpkg -i /tmp/$file

sudo apt install -f

exit
