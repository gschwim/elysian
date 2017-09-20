#!/usr/bin/python

import tsxlib

IP_ADDR = '127.0.0.1'

mount = tsxlib.mount(IP_ADDR)
# print('Try this: %s' % mount.output)
print ('1. %s' % mount.IP_ADDR)
print ('2. %s' % mount.tsxcheck())
print ('3. %s' % mount.is_parked())
print ('4. %s' % mount.output)

try:
    out = mount.tsxcheck()
    print ('Version is: %s' % out)
    out = mount.is_parked()
    print ('Is Parked? %s' % out)
except:
    print ("Didn't work\n")
