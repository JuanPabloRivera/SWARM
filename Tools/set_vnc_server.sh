#!/bin/bash

usage(){
    echo "USAGE: $0 [OPTIONS]"
    echo
    echo "OPTIONS"
    echo 
    echo "    -r, --reboot;    Reboot the system after performing set up"
}

OPTIONS=$(getopt -o r --long reboot -- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$OPTIONS"

reb=false
while true; do
    case "$1" in
        -r | --reboot) reb=true; shift ;;
        --) shift; break;
    esac
done

# Installing required dependencies
sudo apt update
sudo apt install vino

# Enable the VNC server to start each time you log in
mkdir -p ~/.config/autostart
cp /usr/share/applications/vino-server.desktop ~/.config/autostart

# Configure the VNC server
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false

# Set a password to access the VNC server
# Replace thepassword with your desired password
gsettings set org.gnome.Vino authentication-methods "['vnc']"
gsettings set org.gnome.Vino vnc-password $(echo -n 'password'|base64)

#Reboot the system to save changes
if [ "$reb" = true ]; then sudo reboot; exit 0; fi
