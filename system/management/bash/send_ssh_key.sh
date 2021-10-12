#!/bin/bash
IP_addr=$1
myuser=$2
passwd=$3 
echo $IP_addr $myuser $passwd 
ssh_pub=$(cat ~/.ssh/id_rsa.pub)
echo "ici"
{ sleep 2; echo "$passwd"; } | script -q /dev/null -c 'scp -r -p 22 home/rtu/.ssh/id_rsa.pub  $myuser@"$IP_addr":.ssh/authorized_keys '

echo "là"
sudo sshpass -p $passwd scp -r ~/.ssh/id_rsa.pub $myuser@$IP_addr:.ssh/authorized_keys
sleep 4

exit $?
