#!/bin/bash
IP_addr=$1
myuser=$2
passwd=$3 
cat ~/.ssh/id_rsa.pub | sudo sshpass -p $passwd ssh $myuser@$IP_addr  "cat > /home/crown/.ssh/authorized_keys"
exit $?
