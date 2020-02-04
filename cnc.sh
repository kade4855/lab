#!/bin/sh -
#description     :This script will connect(ssh) into 1 device, and collect outputs and store it in ~/cnc_out.txt
#author		 :Kaushal Deodhar
#date            :20181109
#version         :0.1    
#usage		 :cnc "device-name" "command file|command string"
#==============================================================================


# sample cmds input "ls -al | grep config"$'\n'"pwd | head -1"$'\n'"uname | wc"
# ./cnc.sh router-1 'show lldp neighbors | grep "r2|r3"'$'\n''show version | grep "hardware|platform|version"'

host=$1
if [ -f "$2" ]; then
	cmds=`cat $2`
else
	cmds=$2
fi
echo $1
echo $cmds


out_file=$3
echo outputs stored in $out_file
if [ ! -e $out_file ]
then touch $out_file
fi

if [ ! -w $out_file ] || [ ! -r $out_file ]
then chmod u+rw $out_file
fi

#cmds1=''' 
#show version | grep platform
#show interface description
#'''
#echo $cmds1


ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no $host << EOF >> $out_file
$cmds
EOF
