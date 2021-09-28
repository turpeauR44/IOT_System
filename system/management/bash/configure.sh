#!/bin/bash
###############################################################################
#Ce programme a pour but de guide la configuration d'un hote
###############################################################################

###############################################################################
# Variables
###############################################################################
Step=0
hostname_id=0
hostname_mac="00:00:00:00:00"
system_id=0
db="/home/crown/Network/Network.sqlite3"


###############################################################################
# Help
###############################################################################
Help()
(
	#Display Help
	echo "This function allow to follow the configuration of an host taking into account data recorded in the database"
	echo
	echo "Option(s) available(s)"
	echo "t	hostname target"
	echo "d	By default Network/Network.sqlite3 will be tried"
	echo "h	Print this Help"
)

###############################################################################
# Main
###############################################################################

# Options
############################
while getopts "p:t:d:h" option; do
	case $option in
		
		h) # display Help
			Help
			exit;;
		t) # Target selection
			hostname=$OPTARG;;
		d) # Database selection
			db=$OPTARG;;
		p) # local_path selection
			local_path=$OPTARG;;
		\?) # invalid option
			echo "Error: Invalid option"
			exit;;
	esac
done

###############################################################################
# Sources
###############################################################################
. $local_path/colors
. $local_path/messages
. $local_path/configure_functions.sh -d $db 


# Execution
############################
STEP " Hostname 1st Check"
S_init #Cette fonction réinitialise les variables sql
#Le nom de la target doit être passée en option
proceed_step0 #fonction détaillée dans configure_functions
if [ $Step -eq 0 ]; then RESULT "failed at Step${value}$Step${neutre} please proceed again";fi

#A cette étape nous avons récupéré le hostname_id et ses détails pour le système selectionné: system_id
if [ $Step -eq 1 ]; then
#On vérifie à présent que les addresses sont correctes
STEP "Configuration Check"
#On va d'abord scanner notre réseau pour voir si on à un hôte sur notre réseau
proceed_step1 #fonction détaillée dans configure_functions



fi
if [ $Step -eq 1 ]; then RESULT "failed at Step${value}$Step${neutre} please proceed again"; fi 

