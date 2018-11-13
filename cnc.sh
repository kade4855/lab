#!/bin/sh -
#description     :This script will connect(ssh) into 1 device, and collect outputs and store it in ~/tmp/cnc_out.txt
#author		 :Kaushal Deodhar
#date            :20181109
#version         :0.1    
#usage		 :cnc "device-name" "command file|command string"
#==============================================================================


# sample cmds input "ls -al | grep config"$'\n'"pwd | head -1"$'\n'"uname | wc"
# ./cnc.sh dub54-br-agg-r1 'show lldp neighbors | grep "dub2|dub3"'$'\n''show version | grep "hardware|platform|version"'

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
touch ~/cnc_out.txt

ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no $host << EOF > ~/cnc_out.txt
$cmds
EOF
