#!/bin/bash
user="crown"
password="@Crown4884Wmpc"
IPv4="169.254.13.184"

sleep 1; printf "$password\nO\nO\n" | ssh $user@$IPv4 sudo apt-get install git jq
