#!/bin/bash
IP_addr=$1

ping -c 1 $IP_addr > /dev/null

