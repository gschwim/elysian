#!/usr/bin/python

import time
import tsxlib
import tweepy

IP_ADDR = '127.0.0.1'

mount = tsxlib.mount(IP_ADDR)

try:
    mount.tsxcheck()
    mount.is_parked()
    print ("Worked!\n")
except:
    print ("Didn't work\n")
