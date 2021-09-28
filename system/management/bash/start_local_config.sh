#!/bin/bash
#On enregistre une copie de wpa_supplicant_conf
ssid=$1
pwd=$2


wpa_conf="/etc/wpa_supplicant/wpa_supplicant.conf"

if [ -f "$wpa_conf" ]; then sudo chmod 777 $wpa_conf;else echo "missing wpa_supplicant.conf file";exit 1 ;fi
if [ -f "$wpa_conf.sav" ]; then sudo cp "$wpa_conf.sav" "$wpa_conf"; else sudo cp "$wpa_conf" "$wpa_conf.sav"; fi

#On ajoute la nouvelle config
echo -e "network={\n\tssid=\"$ssid\"\n\tpsk=\"$pwd\"\n}" >> $wpa_conf

#On reboot le system
#sudo systemctl restart wpa_supplicant
sudo systemctl restart dhcpcd
