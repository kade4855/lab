#!/usr/bin/env python3

from getpass import getpass, getuser

username = getuser()
password = getpass()

print(username, password)
