#!/usr/bin/python

import socket
import time
import tsxlib as tsx

TCP_PORT = 3040
IP_ADDR = '127.0.0.1'
READBUF = 1024

mount

tsx = connect(IP_ADDR, TCP_PORT, READBUF)
tsx.send(POLL_STATE)
camstate = int(tsx.recv(READBUF).split('|')[0])

while (camstate > 0):
    print "%s : Camera is busy!" % time.strftime("%H:%M:%S")
    time.sleep(60)
    tsx.send(POLL_STATE)
    camstate = int(tsx.recv(READBUF).split('|')[0])

print "Sleeping 900 seconds before shutdown. Cancel if you wish."
time.sleep(60)
print "Camera is no longer busy. Parking mount..."
tsx.send(PARK_MOUNT)
time.sleep(60)
print "Mount should be parked now. Quitting..."

tsx.close()
