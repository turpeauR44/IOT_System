#!/bin/bash
echo $1 $2 $3 $4
IP_addr=$1
myuser=$2
password=$3
myfile="$4"


local_path=/home/crown/System/system/management/files/$myfile
declare -A target_path
#target_path['hostapd']='/etc/default/hostapd'
#target_path['hostapd.conf']='/etc/hostapd/hostapd.conf'
#target_path['hostapd.accept']='/etc/hostapd/hostapd.accept'
#target_path['interfaces']='/etc/network/interfaces'
#target_path['sysctl.conf']='/etc/sysctl.conf'
#target_path['rc.local']='/home/crown/rc.local'
#target_path['pg_hba.conf']='/etc/postgresql/11/main/pg_hba.conf'
#target_path['postgresql.conf']='/etc/postgresql/11/main/postgresql.conf'
pg_hba=""
#echo $local_path target_path[$file]
#sudo sshpass -p $passwd scp  $local_path $myuser@$IP_addr:target_path[$file]


if [ $myfile == "rc.local" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/rc.local"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/rc.local
elif [ $myfile == "postgresql.conf" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/postgresql/11/main/postgresql.conf"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/postgresql/11/main/postgresql.conf
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R postgres /etc/postgresql/11/main/postgresql.conf"
elif [ $myfile == "pg_hba.conf" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/postgresql/11/main/pg_hba.conf"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/postgresql/11/main/pg_hba.conf
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R postgres /etc/postgresql/11/main/pg_hba.conf"
elif [ $myfile == "hostapd" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/default/hostapd"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/default/hostapd
elif [ $myfile == "hostapd.conf" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/hostapd/hostapd.conf"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/hostapd/hostapd.conf
elif [ $myfile == "hostapd.accept" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/hostapd/hostapd.accept"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/hostapd/hostapd.accept
elif [ $myfile == "interfaces" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/network/interfaces"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/network/interfaces
elif [ $myfile == "sysctl.conf" ];then
	sudo sshpass -p $password ssh $myuser@$IP_addr "sudo chown -R crown /etc/sysctl.conf"
	sudo sshpass -p $password scp -r $local_path $myuser@$IP_addr:/etc/sysctl.conf
fi
exit 1
