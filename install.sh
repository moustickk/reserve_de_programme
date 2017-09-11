################################################
# Authors:	Ludovic DUGUE
# On Sept 11 2017
# V0.1
################################################
#!/bin/bash
dirinstall=${PWD}
cp -r $dirinstall/* /$HOME/astro-indi/
cd /$HOME/astro-indi/
chmod +x ./*
