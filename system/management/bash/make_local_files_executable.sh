#!/bin/bash
file=$1
if [ -f $file ]; then sudo chmod +x $file; exit 1; else exit 0; fi

