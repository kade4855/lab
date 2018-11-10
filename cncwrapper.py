#!/usr/bin/env python3

'''
Things to add -
Add verbose options
Add output directory options
Add multithreading

Override 'show' command verification button
'''


#cnc wrapper script

#import
import argparse
import subprocess
import os.path
from sys import exit
#Parse Args
parser = argparse.ArgumentParser(description="Wrapper for cnc.sh")
parser.add_argument("--host", help = "Provide comma-separated hoss names or filename")
parser.add_argument("--cmd", help = "Provide comma-separated commands names or filename")
args = parser.parse_args()

print(args.host)
print(args.cmd)

#Parse input files and create lists

def file_to_list(file_name):
	with open(file_name,'r') as f:
		unformatted_output = [line.strip('\n') for line in f if (line != '\n' and line != '')]
	return [out.strip() for out in unformatted_output]

def string_to_list(input_string):
	string_list = input_string.split(',')
	unformatted_output = [v.strip('\n') for v in string_list if (v != '\n' and v != '')]
	return [out.strip() for out in unformatted_output]

if os.path.isfile(args.host):
	#print('found host file')
	host_list = file_to_list(args.host)
else: host_list = string_to_list(args.host)


if os.path.isfile(args.cmd):
	cmd_list = file_to_list(args.cmd)
else: cmd_list = string_to_list(args.cmd)

print(host_list,cmd_list)

#Verify cmd_list
if all(cmd.startswith("show") for cmd in cmd_list):
	print("commands valid")
	bool_cmd_list = True
else:
	print("missing 'show' for some command")
	exit()

#verify host_list
if host_list:
	bool_host_list = True
else:
	print("no valid hosts")

#Call cnc
if bool_host_list and bool_cmd_list:
	call_cnc(host_list, cmd_list)

	



#Format output cnc_out.txt

