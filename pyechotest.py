#!/usr/bin/env python3

import subprocess

l = ['show lldp neighbors | grep "dub2|dub3"','show config interface | display set | grep "xe-2/"','show version | grep "hardware|platform|version"']
#l = ['ls -al | grep config','pwd | head -1','uname | wc']
for i in range(len(l)-1):
	l.insert(2*i+1,"\n")
s = ''.join(l)
#print(l)
#print(s)

host = "dub54-br-agg-r3"
s = subprocess.run(["/Users/deodhk/githubclone/cnc.sh", host, s])
print('stderr {}'.format(s.stderr))
print('stdout {}'.format(s.stdout))
'''
filename = host+'.txt'
with open(filename, 'w+') as f:
	f.write(s.stdout)
'''
