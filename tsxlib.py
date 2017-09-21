

################################################################################
## This module will provide the base interactions with The Sky X via the
## TCP server.
##
## - class mount() - this class will provide state information of the mount,
##    as well as allow actions to occur e.g. homing, slewing, parking, etc
##
## - class imager() - TODO  - this class will handle all things that are relevant to cameras,
##    focusers, rotators, guiders, etc.
##
#################################################################################

import socket, time

class mount():

    def __init__(self, IP_ADDR='127.0.0.1', TCP_PORT=3040, READBUF=4096, output=''):
        self.IP_ADDR = IP_ADDR
        self.TCP_PORT = TCP_PORT
        self.READBUF = READBUF
        self.output = 'x'

    def send(self, CMD):
        # TODO - connection error handling
        # TODO - logging of actions
        # TODO - Sane output
        # TODO - debug level
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.IP_ADDR, self.TCP_PORT)) # open the socket
            s.send(bytes(JS_HEADER + MNT_ISCONNECTED + JS_FOOTER)) # see if the mount is connected
            state = int(s.recv(self.READBUF).split('|')[0])
            if (state != 1):
                print ('Mount is not connected: %s' % state)
                s.send(JS_HEADER + MNT_CONNECTANDDONOTUNPARK + JS_FOOTER)
                s.recv(self.READBUF)
            s.send(bytes(JS_HEADER + CMD + JS_FOOTER))
            self.output = s.recv(self.READBUF).split('|')
        except:
            self.output = 'Error communicating with mount. State was:\n %s' % state
            return self.output
        else:
            return self.output

    ## START - basic command library

    def tsxCheck(self):
        # TODO - move this to a general app status class or something
        output = self.send(TSX_APPBUILD)
        return self.output

    def tsxQuit(self):
        output = self.send(TSX_QUIT)
        return self.output

    def Connect(self):
        output = self.send(MNT_CONNECT)
        return output

    def Disconnect(self):
        output = self.send(MNT_DISCONNECT)
        return output

    def ConnectAndDoNotUnpark(self):
        output = self.send(MNT_CONNECTANDDONOTUNPARK)
        return output

    def ParkAndDoNotDisconnect(self):
        output = self.send(MNT_PARKANDDONOTDISCONNECT)
        return self.output

    def IsParked(self):
        output = self.send(MNT_ISPARKED)
        return self.output

    def Unpark(self):
        output = self.send(MNT_UNPARK)
        return self.output

    def FindHome(self):
        output = self.send(MNT_FINDHOME)
        return self.output

    ## END - basic command library

    # def park_safely(self):
    #     # 'Safely' is subjective
    #     # This command will do the following as a "safe" park
    #     # 1) tsxcheck() - verify TSX is running
    #     # 2) is_parked() - see if the mount is parked first
    #     # 3) find_home() - this make sure we know where we are
    #     # 4) parkdnd() - park and don't disconnect.
    #     # 5) is_parked() - see if we're parked again.
    #
    #     # TODO - trap on TSX not being up
    #     self.tsxcheck()
    #     # TODO - if parked, do we really want to home?
    #     # TODO - verify that parked and appropriate absolute position match
    #     self.is_parked()
    #     # TODO - would be nice to know for certain that we're homed
    #     # - might need an ask to Bisque
    #     self.find_home()
    #     self.parkdnd()
    #     # TODO - throw an exception if it does not show parked
    #     # TODO - verify absolute position as above
    #     self.is_parked()


## Here be the base commands from tsx

JS_HEADER = '/* Java Script */\n/* Socket Start Packet */\n'
JS_FOOTER = '\n/* Socket End Packet */\n'

## TSX Misc functions

TSX_APPBUILD = 'Application.build'
TSX_QUIT = 'sky6RASCOMTheSky.Quit()'

## MOUNT

MNT_PREAMBLE = 'sky6RASCOMTele'
MNT_ISCONNECTED = '%s.IsConnected;\n' % MNT_PREAMBLE
MNT_ASYNCHRONOUS_ON = '%s.Asynchronous = 1\n' % MNT_PREAMBLE
MNT_ASYNCHRONOUS_OFF = '%s.Asynchronous = 0\n' % MNT_PREAMBLE
MNT_ASYNCHRONOUS = '%s.Asynchronous\n'
MNT_CONNECT = '%s.Connect();\n' % MNT_PREAMBLE
MNT_DISCONNECT = '%s.Disconnect();\n' % MNT_PREAMBLE
MNT_CONNECTANDDONOTUNPARK = '%s.ConnectAndDoNotUnpark();\n' % MNT_PREAMBLE
MNT_PARK = '%s.Park();\n' % MNT_PREAMBLE
MNT_PARKANDDONOTDISCONNECT = '%s.ParkAndDoNotDisconnect();\n' % MNT_PREAMBLE
MNT_ISPARKED = '%s.IsParked();\n' % MNT_PREAMBLE
MNT_UNPARK = '%s.Unpark();\n' % MNT_PREAMBLE
MNT_FINDHOME = '%s.FindHome();\n' % MNT_PREAMBLE
