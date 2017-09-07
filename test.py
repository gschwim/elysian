#!/usr/bin/python

import time
import tsxlib

IP_ADDR='172.16.254.254'

mount = tsxlib.mount(IP_ADDR)

mount.park_safely()


# mount.unpark()
# mount.is_parked()
# mount.parkdnd()
# mount.is_parked()
# mount.unpark()
# time.sleep(5)
# print 'Finding home...\n'
# mount.find_home()
# print 'Is it homed yet?\n'
# time.sleep(5)
# print 'Parking\n'
# mount.is_parked()
# mount.parkdnd()
# mount.is_parked()
# print 'Done\n'
