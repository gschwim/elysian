#!/usr/bin/python3

import tsxlib, time

IP_ADDR = '172.16.254.254'
mount = tsxlib.mount(IP_ADDR)
iteration = 1

while (1):
    print ('###### Iteration #%s #######' % iteration)
    print ('1. Talking to: %s' % mount.IP_ADDR)
    print ('2. Version: %s  ' % mount.tsxCheck())
    print ('3. Mount parked: %s' % mount.IsParked())
    print ('4. Park mount: %s' % mount.ParkAndDoNotDisconnect())
    print ('5. Mount parked: %s' % mount.IsParked())
    print ('6. Disconnect mount: %s' % mount.Disconnect())
    time.sleep(5)
    iteration += 1





