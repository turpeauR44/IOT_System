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
