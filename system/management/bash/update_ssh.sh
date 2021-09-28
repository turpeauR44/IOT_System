#!/bin/bash
###############################################################################
#Ce programme a pour but d'enregistrer une nouvelle clé ssh avec son mot de passe dans la clé cryptée
###############################################################################

###############################################################################
# Variables
###############################################################################
driver="sda"
network="crown"

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
. Initialisation/sql_network.sh
echo $System_id
# Close current ext_keys decrypt
sudo cryptsetup luksClose ext_keys > /dev/null 2>&1
# Request password to user
read -s -p "please provide USB Key Password: " passw; echo
#Start driver:
printf "$passw" | sudo cryptsetup luksOpen /dev/$driver ext_keys > /dev/null 2>&1
#Mount external drive
sudo mount -t ext2 -o noatime /dev/mapper/ext_keys /mnt/ext_keys > /dev/null 2>&1

#Password generation
mymdp=$(openssl rand -base64 32)
sudo mkdir -m 777 -p /mnt/ext_keys/$HOSTNAME/ssh 
sudo touch /mnt/ext_keys/$HOSTNAME/ssh/.new_ssh_pass
sudo chmod 777 /mnt/ext_keys/$HOSTNAME/ssh/.new_ssh_pass 
sudo echo -ne $mymdp > /mnt/ext_keys/$HOSTNAME/ssh/.new_ssh_pass 

# Record of the new ssh_key in the crypted drive:
printf "y" | sudo ssh-keygen -f /mnt/ext_keys/$HOSTNAME/ssh/new_id_rsa -P "$mymdp"

#Start ssh-agent and add current ssh_key
old_ssh_key=$(cat /mnt/ext_keys/$HOSTNAME/ssh/.cur_ssh_pass)
eval $(ssh-agent -s)
{ sleep .1; echo $old_ssh_key; } | script -q /dev/null -c 'ssh-add .ssh/id_rsa'


# Add the public key on different hosts connected

# Remove previous key 

#Umount driver
#sudo umount /mnt/ext_keys
#sync
