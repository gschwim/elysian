#!/usr/bin/python3

import tsxlib, time, json

IP_ADDR = '172.16.254.254'
mount = tsxlib.mount(IP_ADDR)


def test1(count):
    iteration = 1
    while (iteration < count):
        print('###### Iteration #%s #######' % iteration)
        print('1. Talking to: %s' % mount.IP_ADDR)
        print('2. Version: %s  ' % mount.tsxCheck())
        print('3. Mount parked: %s' % mount.IsParked())
        print('4. Park mount: %s' % mount.ParkAndDoNotDisconnect())
        print('5. Mount parked: %s' % mount.IsParked())
        print('6. Disconnect mount: %s' % mount.Disconnect())
        print('Sleeping...\n\n')
        time.sleep(5)
        iteration += 1

def test2():
    data = mount.GetStatus()
    print('Raw Data: %s' % data)
    for key in data:
        print('Keys found: %s' % key)
        for subkey in data[key]:
            print(subkey + ': ' + data[key][subkey])

def test3():
    data = mount.IsParked()
    print('Data is: %s' % data)

test1(3)
# test2()
# test3()

