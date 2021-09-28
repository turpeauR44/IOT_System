S_init(){
	networks_id=()
	networks_addr=()
	systems_id=()
	systems_desi=()
}

S0_get_hostname_id(){
	echo ".timeout 2000
	SELECT id FROM TAB_HOSTS where hostname='$hostname';
.exit" | sqlite3 ${db} > resultsql
	IFS="|"
	if test -s "resultsql";then
		while read LINE;do
		set $LINE
		hostname_id=$1;done < resultsql;fi
}
S0_get_host_networks(){
        echo ".timeout 2000
        SELECT THN.network_id, THN.IPv4 FROM TAB_HOST_NETWORKS as THN
        LEFT JOIN TAB_NETWORKS as TN on TN.id=network_id
        LEFT JOIN TAB_NETWORKCARDS as TNC on TNC.id=THN.networkcard_id
	where TNC.host_id='$hostname_id';
.exit" | sqlite3 ${db} > resultsql
        IFS="|"
        if test -s "resultsql";then
                while read LINE;do
                set $LINE
                networks_id+=($1);networks_addr=($2);done < resultsql;fi
}
S0_get_host_systems(){
	echo ".timeout 2000
        SELECT DISTINCT TS.id,TS.desi FROM TAB_HOST_NETWORKS as THN
	LEFT JOIN TAB_NETWORKS as TN on TN.id = network_id
		LEFT JOIN TAB_SYSTEMS as TS on TS.id=TN.system_id
        LEFT JOIN TAB_NETWORKCARDS as TNC on TNC.id=THN.networkcard_id
	 where TNC.host_id='$hostname_id';
.exit" | sqlite3 ${db} > resultsql
        IFS="|"
        if test -s "resultsql";then
                while read LINE;do
                set $LINE
                systems_id+=($1);systems_desi+=($2);done < resultsql;fi

}

proceed_step0(){
if [ "$hostname" = "" ]; then STOP "option -t hostname required";
#On vérifie ici que l'on cible le bon système
else PROCEED "looking for host: ${value}$hostname${neutre} in Network database"
	S0_get_hostname_id
	if [ $hostname_id -eq 0 ]; then STOP "there is no host : ${value}$hostname${neutre} recorded in ${value}$db";
	else S0_get_host_networks
		if [ ${#networks_id[@]} -eq 0 ]; then STOP "No network attributed to this host"
			else S0_get_host_systems
			if [ ${#systems_id[@]} -eq 0 ]; then STOP "No system attributed to this host"
			elif [ ${#systems_id[@]} -eq 1 ]; then QUESTION "please confirm that you want to configure host : ${value}$hostname${neutre} for system ${value}${systems_desi[0]}${neutre}"
				read -p "TYPE y TO CONFIRM : " answer
				if [ "$answer" != "y" ]; then STOP "update database if needed"
					else system_id=${systems_id[0]} 
Step=1;			fi
			else QUESTION "please select system in the following list:"
				for (( num_system=1; num_system<${#systems_id[@]}+1; num_system++)); do
					echo -e "${systems_desi[$num_system-1]}\t\t--> \t\t $num_system"
				done
				read -p "PLEASE GIVE A NUMBER BETWEEN 1 AND ${#systems_id[@]} : " answer
				for (( num_system=1; num_system<${#systems_id[@]}+1; num_system++)); do
					if [ "$answer" = "$num_system" ]; then system_id=${systems_id[$num_system-1]};
Step=1; 			fi
				done
				if [ $system_id -eq 0 ]; then STOP "Wrong inpput";fi
			fi
		fi	
	fi
fi	
}

proceed_step1(){
#On commence par extraire notre table arp:
arp -a -v > arpresult	
}
