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
import re
import argparse
import logging
import os.path 
from subprocess import run
from sys import exit
from shutil import copy2

#Parse Args
example_input = '''Example:
cncwrapper.py -host 'host1, host2' -cmd 'show_cmd1, show_cmd2' -out 'output_file'
cncwrapper.py -host hostinputfile.txt --cmd cmdinputfile.txt --out testfile

Sample:
cncwrapper.py -host 'router-1, router-2' -cmd ' show configuration interfaces | display set | grep "xe-2/| ae", show lldp neighbor | grep "dub2|dub3"'

'''
parser = argparse.ArgumentParser(description="Wrapper for cnc.sh",
								 epilog= example_input,
								 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-host", help = "Provide comma-separated host names in single quotes or filename")
parser.add_argument("-cmd", help = "Provide comma-separated commands names in single quotes or filename")
parser.add_argument("-int", help = "Provide comma-separated interface names in single quotes or filename")
parser.add_argument("-out", help = "Provide output filename(optional), if no filename - outputs will be stored in separate files for each device under home directory")
parser.add_argument("-v", help = "For debugs", action="store_true")
args = parser.parse_args()

if args.v:
	logging.basicConfig(level=logging.DEBUG)

logging.debug("\thost input - \n{}\n".format(args.host))
logging.debug("\tcommands input - \n{}\n".format(args.cmd))
logging.debug("\toutput file - \n{}\n".format(args.out))

#intf_cmds = '''show chassis pic fpc-slot {fpc} pic-slot {pic}
#show interface diagnostic optics {intf} | except "threshold|off"
#show config interface {intf} | display set
#show interface terse {intf}
#show lldp neighbor interface {intf}
#show lacp interfaces {intf}
#show log messages | grep {intf}
#'''

intf_cmds = '''show interface description {intf}
show lldp neighbor interface {intf}
show configuration interface {intf}
show interface terse {intf}
'''

def file_to_list(file_name):
	with open(file_name,'r') as f:
		unformatted_output = [line.strip('\n') for line in f if (line != '\n' and line != '')]
	return [out.strip() for out in unformatted_output]

def string_to_list(input_string):
	string_list = input_string.split(',')
	unformatted_output = [v.strip('\n') for v in string_list if (v != '\n' and v != '')]
	return [out.strip() for out in unformatted_output]

def parse_input_args(inpt):
	#determine_input_file_or_string
	if os.path.isfile(inpt):
		logging.debug("\t Found file - {}".format(inpt))
		return file_to_list(inpt)
	else:
		logging.debug("\t Using input as string - {}".format(inpt))
		return string_to_list(inpt)


#Verify cmd_list
def verify_cmd_list(cmd_list):
	verified_cmd_list = [cmd for cmd in cmd_list] #if cmd.startswith("show")]
	if len(cmd_list) != len(verified_cmd_list):
		logging.warning("missing 'show' for some command, only using valid show commands")
	if verified_cmd_list: return verified_cmd_list
	else:
		logging.error("no valid commands found") 
		exit()

#verify host_list
def verify_host_list(host_list):
	verified_host_list = list(set(host_list))
	if verified_host_list: return verified_host_list
	else:
		logging.error("no valid hosts found")
		exit()

#Convert verified_cmd_list/verified_int_list to string(cnc.sh consumable)
def convert_verified_list_to_string(verified_list):
	verified_string = ''
	for i in range(len(verified_list)-1):
		verified_list.insert(2*i+1,"\n")
	verified_string = ''.join(verified_list)
	return verified_string

def verified_int_cmd_string(int_list):
	verified_int_cmd_string = ''
	int_cmd_string = ''
	print(int_list)
	for intf in int_list:
		if 'xe' in intf:
			intf_r = re.match(r'xe-(?P<fpc>[\d]+)/(?P<pic>[\d]+)/(?P<slot>[\d]+)',intf)
			unformatted_intf_cmds = intf_cmds.format(intf = intf_r.string,fpc = intf_r.group('fpc'),pic = intf_r.group('pic'))
			int_cmd_string += unformatted_intf_cmds
	verified_int_cmd_list = list(set(int_cmd_string.splitlines()))
	return convert_verified_list_to_string(verified_int_cmd_list)

#Call cnc to run ssh on each host
def call_cnc(verified_host_list, verified_cmd_string):
	home = os.path.expanduser("~")
	module_dir = os.path.dirname(os.path.realpath(__file__))
	for host in verified_host_list:
		if args.out: 	output_file = home+'/'+args.out
		else:	output_file=home+'/'+host+'.txt'
		sub = run([module_dir+"/cnc.sh", host, verified_cmd_string, output_file])
#		copy2(home+'/cnc_out.txt',home+'/'+host+'.txt')
#		print("output stored in {}".format(home+'/'+host+'.txt'))


'''
Step 1: 
Gather input from file or cmdline args
Parse input(hosts and commands) and convert to lists
'''

#if "__name__" == "__main__":
'''
bool_host_input = False
bool_cmd_input = False
bool_int_input = False
'''

if args.host:
	host_list = parse_input_args(args.host)
	#Verify host_list
	verified_host_list = verify_host_list(host_list)
	logging.info("\nverified_host_list:\n {}\n".format(verified_host_list))
else:
	logging.error("\trequire host input")
	exit()

#if args.cmd or args.int:
if args.cmd:
	cmd_list = parse_input_args(args.cmd)
	verified_cmd_list = verify_cmd_list(cmd_list)
	verified_cmd_string = convert_verified_list_to_string(verified_cmd_list)
	logging.info("\nverified_cmd_string:\n {}\n".format(verified_cmd_string))
	call_cnc(verified_host_list, verified_cmd_string)
elif args.int:
	logging.debug('\tInterface args found')
	int_list = parse_input_args(args.int)
	logging.debug = ("\t interface list - {}".format(int_list))
	verified_int_cmd_string = verified_int_cmd_string(int_list)
	if args.v:
		print(verified_int_cmd_string)
	call_cnc(verified_host_list, verified_int_cmd_string)
#call int_method
else:
	logging.error("\trequire cmd or interface input")
	exit()

exit()
#check if output file already present and 'info' about overwritting 


#xe-(?P<fpc>[\d])/(?P<pic>[\d])/(?P<slot>[\d])


