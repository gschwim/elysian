

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

import socket, time, json

class mount():

    def __init__(self, IP_ADDR='127.0.0.1', TCP_PORT=3040, READBUF=4096, output=''):
        self.IP_ADDR = IP_ADDR
        self.TCP_PORT = TCP_PORT
        self.READBUF = READBUF
        self.output = 'x'

    def send(self, CMD):
        # TODO - connection error handling <- is the below sufficient?
        # TODO - logging of actions
        # TODO - Sane output <- moving towards dict
        # TODO - debug level
        # TODO - may need to break out send/conn handling so we can prevent recursive loops
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10) # TODO - why did I put this in here? Bisque says wait > script timeout of 300s?
        try:
            s.connect((self.IP_ADDR, self.TCP_PORT)) # open the socket
            s.send((JS_HEADER + MNT_ISCONNECTED + JS_FOOTER).encode('utf8')) # see if the mount is connected
            state = int(((s.recv(self.READBUF)).decode('utf8')).split('|')[0].strip())
            if (state != 1):
                #print ('Mount is not connected: %s' % state)
                s.send((JS_HEADER + MNT_CONNECTANDDONOTUNPARK + JS_FOOTER).encode('utf8'))
                s.recv(self.READBUF)
            s.send((JS_HEADER + CMD + JS_FOOTER).encode('utf8')) # send the command
            self.output = (s.recv(self.READBUF)).decode('utf8').split('|')[0].strip()
            # TODO - need some error handling here for the right side of the response (self.output[1])
            # TODO - thinking that this might just be in the dict for response, let the client split it
        except:
            # TODO - give some more useful error handling here
            self.output = 'ERROR'
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
        data = self.send(MNT_ISPARKED)
        output = {
            'parked': data
        }
        return output

    def IsConnected(self):
        data = self.send(MNT_ISCONNECTED)
        if data == 'ERROR':
            return data
        elif int(data) == 1:
            data = 'true'
        elif int(data) == 0:
            data = 'false'
        output = { 'connected': data }
        return output

    def Unpark(self):
        output = self.send(MNT_UNPARK)
        return self.output

    def FindHome(self):
        output = self.send(MNT_FINDHOME)
        return self.output

    def GetAzAlt(self):
        data = self.send(MNT_GETAZALT).split(',')
        output = {
            'azimuth' : data[0],
            'altitude' : data[1]
        }
        return output

    def GetRaDec(self):
        data = self.send(MNT_GETRADEC).split(',')
        output = {
            'ra': data[0],
            'dec': data[1]
        }
        return output

    def GetTrackingStatus(self):
        data_rate = self.send(MNT_GETTRACKINGRATE).split(',')
        data_is_tracking = self.send(MNT_ISTRACKING)
        if int(data_is_tracking) == 1:
            data_is_tracking = 'true'
        else:
            data_is_tracking = 'false'
        output = {
            'is_tracking': data_is_tracking,
            'tracking_rate_Ra': data_rate[0],
            'tracking_rate_Dec': data_rate[1]
        }
        return output

    def IsSlewComplete(self):
        data = self.send(MNT_ISSLEWCOMPLETE)
        # treating this as slew status, true = slewing
        # Is it doing it or not, not is it done doing it. Inconsistencies!!
        if int(data) == 1:
            data = 'false'
        else:
            data = 'true'
        output = { 'slew': data }
        return output

    def GetStatus(self):
        status_connection = self.IsConnected()
        if status_connection == 'ERROR':
            output = {
                'Polltime': time.ctime(),
                'Connected': {'connected': 'ERROR'},
                'Parked': '',
                'Slewing': '',
                'Tracking': '',
                'AzAlt': '',
                'RaDec': ''

            }
            return output
        else:
            status_parked = self.IsParked()
            status_slewing = self.IsSlewComplete()
            status_tracking = self.GetTrackingStatus()
            status_AzAlt = self.GetAzAlt()
            status_RaDec = self.GetRaDec()
            output = {
                'Polltime': {
                    'epoch': time.time(),
                    'ctime': time.ctime()
                },
                'Connected': status_connection,
                'Parked': status_parked,
                'Slewing': status_slewing,
                'Tracking': status_tracking,
                'AzAlt': status_AzAlt,
                'RaDec': status_RaDec

            }
            return output

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
MNT_PREAMBLE = 'sky6RASCOMTele'
THESKY_PREAMBLE = 'sky6RASCOMTheSky'

## TSX Misc functions

TSX_APPBUILD = 'Application.build'
TSX_QUIT = 'sky6RASCOMTheSky.Quit()'

## MOUNT CONTROL CONSTANTS

MNT_ISCONNECTED = '%s.IsConnected;\n' % MNT_PREAMBLE
MNT_ASYNCHRONOUS_ON = '%s.Asynchronous = 1\n' % MNT_PREAMBLE
MNT_ASYNCHRONOUS_OFF = '%s.Asynchronous = 0\n' % MNT_PREAMBLE
MNT_ASYNCHRONOUS = '%s.Asynchronous\n'
MNT_CONNECT = '%s.Connect();\n' % MNT_PREAMBLE
MNT_DISCONNECT = '%s.DisconnectTelescope();\n' % THESKY_PREAMBLE
MNT_CONNECTANDDONOTUNPARK = '%s.ConnectAndDoNotUnpark();\n' % MNT_PREAMBLE
MNT_PARK = '%s.Park();\n' % MNT_PREAMBLE
MNT_PARKANDDONOTDISCONNECT = '%s.ParkAndDoNotDisconnect();\n' % MNT_PREAMBLE
MNT_ISPARKED = '%s.IsParked();\n' % MNT_PREAMBLE
MNT_UNPARK = '%s.Unpark();\n' % MNT_PREAMBLE
MNT_FINDHOME = '%s.FindHome();\n' % MNT_PREAMBLE
MNT_ISTRACKING = 'Out = String(%s.IsTracking);' % MNT_PREAMBLE
MNT_ISSLEWCOMPLETE = 'Out = String(%s.IsSlewComplete);' % MNT_PREAMBLE
# TODO clean up and use MNT_PREAMBLE below
MNT_GETAZALT = '%s.GetAzAlt();\n' \
               'Out  = String(sky6RASCOMTele.dAz) + "," + String(sky6RASCOMTele.dAlt);\n' % MNT_PREAMBLE
MNT_GETRADEC = '%s.GetRaDec();\n' \
               'Out  = String(sky6RASCOMTele.dRa) + "," + String(sky6RASCOMTele.dDec);\n' % MNT_PREAMBLE
MNT_GETTRACKINGRATE = 'Out = String(sky6RASCOMTele.dRaTrackingRate) + "," + String(sky6RASCOMTele.dDecTrackingRate);'
