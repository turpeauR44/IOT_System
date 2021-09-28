#!/bin/bash
if [ -f $1 ]; then echo -e $2 >> $1; exit 1 ; else exit 0; fi


