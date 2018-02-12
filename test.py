#!/usr/bin/python3

import tsxlib, time, json

IP_ADDR = '127.0.0.1'
mount = tsxlib.mount(IP_ADDR)
camera = tsxlib.camera(IP_ADDR)

def camtest1():
    result = camera.GetTempStatus()
    print(result)
    #print('Command result: %s\nScript result: %s ' % (str(result[0]), str(result[2])))

def focus():
    result = camera.AtFocus3()
    print(result)


camtest1()
focus()


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

def test3(count):
    iteration = 1
    while (iteration < count):
        data = mount.GetStatus()
        print('Data is: %s' % data)
        time.sleep(1)
        iteration += 1

#test1(3)
#test2()
#test3(100)

