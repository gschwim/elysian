#!/usr/bin/python

import time
import tsxlib

IP_ADDR='172.16.254.254'

mount = tsxlib.mount(IP_ADDR)

mount.tsxcheck()
