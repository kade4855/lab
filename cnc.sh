#!/bin/sh -
#description     :This script will connect(ssh) into 1 device, and collect outputs and store it in ~/tmp/cnc_out.txt
#author		 :Kaushal Deodhar
#date            :20181109
#version         :0.1    
#usage		 :cnc "device-name" "command file|command string"
#==============================================================================


# sample cmds input "ls -al | grep config"$'\n'"pwd | head -1"$'\n'"uname | wc"

host=$1
if [ -f "$2" ]; then
	cmds=`cat $2`
else
	cmds=$2
fi
echo $1
echo $cmds

#cmds1=''' 
#show version | grep platform
#show interface description
#'''
#echo $cmds1

ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no $host << EOF > ~/tmp/cnc_out.txt
$cmds
EOF
