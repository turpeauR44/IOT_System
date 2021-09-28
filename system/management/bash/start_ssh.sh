#!/bin/bash

###############################################################################
#Ce programme a pour but de charger le mot de passe contenu dans la clef USB cryptée pui de lancer l'agent ssh
###############################################################################


###############################################################################
# Variables
###############################################################################
driver="sda"

###############################################################################
# Help
###############################################################################
Help()
(
	#Display Help
	echo "This function extract the password from the USB Key and start the ssh-agent of this host"
	echo
	echo "Option(s) available(s)"
	echo "s	By default sda will be tried"
	echo "h	Print this Help"
)

###############################################################################
# Main
###############################################################################

# Options
############################
while getopts "s:h" option; do
	case $option in
		
		h) # display Help
			Help
			exit;;
		s) # Driver selection
			driver=$OPTARG;;
		\?) # invalid option
			echo "Error: Invalid option"
			exit;;
	esac
done

# Execution
############################
id_add=$(ssh-add -l | grep SHA256 | grep "$HOSTNAME")
if [ -n "$id_add" ]; then exit 0 ; fi

# Close current ext_keys decrypt
sudo cryptsetup luksClose ext_keys > /dev/null 2>&1
lsblk | grep sd
read -p "please provide driver: " driver; echo
# Request password to user
read -s -p "please provide USB Key Password: " passw; echo
#Start driver:
printf "$passw" | sudo cryptsetup luksOpen /dev/$driver ext_keys  > /dev/null 2>&1
#Mount driver
sudo mount /dev/mapper/ext_keys /mnt/ext_keys  > /dev/null 2>&1
#Extract ssh_key
ssh_key=$(cat /mnt/ext_keys/$HOSTNAME/.ssh_key )
#Umount driver
sudo umount /mnt/ext_keys
sync

eval $(ssh-agent -s)  > /dev/null 2>&1
{ sleep .1; echo $ssh_key; } | script -q /dev/null -c 'ssh-add .ssh/id_rsa' > /dev/null 2>&1
id_add=$(ssh-add -l | grep SHA256 | grep "$HOSTNAME")
if [ -n "$id_add" ]; then exit 0 ; fi

exit 1
