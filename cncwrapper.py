#!/usr/bin/env python3

'''
Author - Kaushal Deodhar

Things to add -
Interface outputs 
Add verbose options
Add output directory options
Add multithreading
Add password/odin
Override 'show' command verification button
'''


#cnc wrapper script

import argparse
import os.path 
from subprocess import run
from sys import exit
from shutil import copy2

#Parse Args
example_input = '''Example:
cncwrapper.py --host 'host1, host2' --cmd 'show_cmd1, show_cmd2'
cncwrapper.py --host hostinputfile.txt --cmd cmdinputfile.txt

Sample:
cncwrapper.py --host 'router-1, router-2' --cmd ' show configuration interfaces | display set | grep "xe-2/| ae", show lldp neighbor | grep "dub2|dub3"'

'''
parser = argparse.ArgumentParser(description="Wrapper for cnc.sh",
								 epilog= example_input,
								 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--host", help = "Provide comma-separated host names in single quotes or filename")
parser.add_argument("--cmd", help = "Provide comma-separated commands names in single quotes or filename")
parser.add_argument("--int", help = "Provide comma-separated interface names in single quotes or filename")
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

def determine_input_file_or_string(inpt):
	if os.path.isfile(inpt):
		return file_to_list(inpt)
	else: return string_to_list(inpt)

#Verify cmd_list
def verify_cmd_list(cmd_list):
	verified_cmd_list = [cmd for cmd in cmd_list if cmd.startswith("show")]
	if len(cmd_list) != len(verified_cmd_list):
		print("missing 'show' for some command, only using valid show commands")
	if verified_cmd_list: return verified_cmd_list
	else:
		print("no valid commands found") 
		exit()

#verify host_list
def verify_host_list(host_list):
	verified_host_list = list(set(host_list))
	if verified_host_list: return verified_host_list
	else:
		print("no valid hosts found")
		exit()

#Convert verified_cmd_list to string(cnc.sh consumable)
def convert_verified_cmd_list_to_string(verified_cmd_list):
	verified_cmd_string = ''
	for i in range(len(verified_cmd_list)-1):
		verified_cmd_list.insert(2*i+1,"\n")
	verified_cmd_string = ''.join(verified_cmd_list)
	global bool_cmd_input
	bool_cmd_input = True
	return verified_cmd_string

#Call cnc to run ssh on each host
#Copy output from ~/cnc_out.txt to new file named ~/<host>.txt
def call_cnc(verified_host_list, verified_cmd_string):
	home = os.path.expanduser("~")
	module_dir = os.path.dirname(os.path.realpath(__file__))
	for host in verified_host_list:
		sub = run([module_dir+"/cnc.sh", host, verified_cmd_string])
		copy2(home+'/cnc_out.txt',home+'/'+host+'.txt')
		print("output stored in {}".format(home+'/'+host+'.txt'))

'''
Step 1: 
Gather input from file or cmdline args
Parse input(hosts and commands) and convert to lists
'''

#if "__name__" == "__main__":
bool_host_input = False
bool_cmd_input = False
bool_int_input = False

if args.host:
	host_list = determine_input_file_or_string(args.host)
	#Verify host_list
	verified_host_list = verify_host_list(host_list)
	print("\nverified_host_list:\n {}\n".format(verified_host_list))
else:
	print("require host input")
	exit()

if args.cmd or args.int:
	if args.cmd:
		cmd_list = determine_input_file_or_string(args.cmd)
		#verify cmd_list
		verified_cmd_list = verify_cmd_list(cmd_list)
		#convert verifed host list to string
		verified_cmd_string = convert_verified_cmd_list_to_string(verified_cmd_list)
		print("\nverified_cmd_string:\n {}\n".format(verified_cmd_string))
	elif args.int:
		print('args found')
	#call int_method
else:
	print("require cmd or interface input")
	exit()


'''
Step 3:
Call cnc.sh for every host
Copy the output from ~/tmp/cnc_out.txt to new ~/<hostname>.txt file
'''
if bool(bool_cmd_input):
	print("calling cnc")
	call_cnc(verified_host_list, verified_cmd_string)
else:
	print("somethings wrong")
exit()




