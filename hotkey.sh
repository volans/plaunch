#!/usr/bin/env bash

lock_file="/tmp/plaunch_lock"
if [ ! -e $lock_file ]
then
    echo "plaunch" >$lock_file
else
    exit 0
fi
