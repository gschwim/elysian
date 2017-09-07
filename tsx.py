#!/usr/local/bin/python3

import socket
import time

READBUF=2048

class TSXConnection(object):
    """
    No idea what I'm doing here.
    """
    def __init__(self, IP_ADDR='127.0.0.1', PORT=3040):
        self.ip = IP_ADDR
        self.port = PORT
        try:
            print 'opening the socket!\n'
            self.sock.connect((self.ip, self.port))
        except socket.error,msg:
            raise 'Cannot connect\n'



    def connect (self):
        ### Basic connection establishment
        ### TODO - do we need READBUF here? Maybe globally set the readbuf size?
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP_ADDR, TCP_PORT))
        return sock

    def send(COMMAND):
        ### This is a basic send command that will be used by other comments to
        ### er, send commands to TSX!
        cmd = COMMAND.encode()
        sockobj.send(bytes('/* Java Script */\n' +
                           '/* Socket Start Packet */\n' +
                           '\n/* Socket End Packet */\n'))
        result = sockobj.recv(2048)
        print(result)
        return result.split("|")[0]
