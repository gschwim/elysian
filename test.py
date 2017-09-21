#!/usr/bin/python

import tsxlib

IP_ADDR = '127.0.0.1'
mount = tsxlib.mount(IP_ADDR)


print ('1. Talking to: %s' % mount.IP_ADDR)
print ('2. Version: %s  ' % mount.tsxCheck())
print ('3. Mount parked: %s' % mount.IsParked())
print ('4. Disconnect mount: %s' % mount.Disconnect())




