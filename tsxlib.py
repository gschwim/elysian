

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

    def send(self, CMD, async=1):
        # TODO - connection error handling <- is the below sufficient?
        # TODO - logging of actions
        # TODO - Sane output <- moving towards dict
        # TODO - debug level
        # TODO - may need to break out send/conn handling so we can prevent recursive loops

        # This method is called by the other methods of the class
        # It handles the socket connection and sending commands
        # as well as receiving the output. One command is intended to be passed
        # through at a time such that all logic is handled here or in the client
        # and not with TSX.
        #
        # DEFAULTS:
        # async = 1 because async behavior is easier to deal with

        # define the socket and try connecting to it
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10) # TODO - why did I put this in here? Bisque says wait > script timeout of 300s?
        try:
            time.sleep(.25) # TSX seems to balk at fast commands from time to time
            s.connect((self.IP_ADDR, self.TCP_PORT)) # open the socket
            s.send((JS_HEADER + MNT_ISCONNECTED
                    + JS_FOOTER).encode('utf8')) # see if the mount is connected
            state = ((s.recv(self.READBUF)).decode('utf8')).split('|')
            #print("%s // %s" % (state[0], state[1]))

            # Test that TSX is connected to the mount. If not, try 3x to make it do that.
            iteration = 1
            while (int(state[0]) != 1 and iteration <= 3):
                # attempt to make the connection
                #print('Not connected. Trying...')
                time.sleep(.5)
                s.send((JS_HEADER + MNT_CONNECTANDDONOTUNPARK + JS_FOOTER).encode('utf8'))
                s.recv(self.READBUF) #clear the buffer. TODO - There must be a cleaner way...

                # ask if the mount is connected now
                s.send((JS_HEADER + MNT_ISCONNECTED + JS_FOOTER).encode('utf8'))
                state = ((s.recv(self.READBUF)).decode('utf8')).split('|')
                #print("Can't connect to mount: %s // %s" % (state[0], state[1]))
                iteration += 1

            # if we still can't get a connection, return an error
            if (int(state[0]) != 1):
                #print('state is %s' % state)
                self.output = tsx_rational_errors(state)
                return self.output

        except:
            # print('failed to open socket')

            # socket could not be open, return an error in the same format as TSX for consistency
            self.output = tsx_rational_errors(('6666', 'Error connecting to TSX!'))
            return self.output
        else:
            # things must be going peachy. Let's do some work!

            # test if async should be on or off. Default is ON.
            if async == 0:
                # someone wants async commands turned off!
                print('Turning Async off')
                s.send((JS_HEADER + MNT_ASYNCHRONOUS_OFF + JS_FOOTER).encode('utf8'))
                s.recv(self.READBUF) # TODO - clear the buffer more cleanly
                s.send((JS_HEADER + CMD + JS_FOOTER).encode('utf8'))  # send the command
            else:
                s.send((JS_HEADER + CMD + JS_FOOTER).encode('utf8'))
            self.output = tsx_rational_errors((s.recv(self.READBUF)).decode('utf8').split('|'))

            return self.output

    ## START - basic command library

    def tsxCheck(self):
        # TODO - move this to a general app status class or something
        output = self.send(TSX_APPBUILD)
        return output

    def tsxQuit(self):
        output = self.send(TSX_QUIT)
        return output

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
        return output

    def IsParked(self):
        data = self.send(MNT_ISPARKED)

        output = {
            'parked': data[0]
        }
        # print(output)
        return output

    def IsConnected(self):
        data = self.send(MNT_ISCONNECTED)[0]
        if int(data) == 1:
            data = 'true'
        elif int(data) == 0:
            data = 'false'
        else:
            data = 'ERROR'
        output = { 'connected': data }
        #print(output)
        return output

    def Unpark(self):
        output = self.send(MNT_UNPARK)
        return output

    def FindHome(self):
        output = self.send(MNT_FINDHOME)
        return output

    def GetObjInfoName(self):
        output = self.send(MNT_OBJINFO_NAME)[0]
        return output

    def GetAzAlt(self):
        data = self.send(MNT_GETAZALT)[0].split(',')
        output = {
            'azimuth' : data[0],
            'altitude' : data[1]
        }
        #print(output)
        return output

    def GetRaDec(self):
        data = self.send(MNT_GETRADEC)[0].split(',')
        output = {
            'ra': data[0],
            'dec': data[1]
        }
        #print(output)
        return output

    def OTASideOfPier(self):
        data = self.send(MNT_SIDEOFPIER)[0]
        if data == '1':
            output = 'west'
        elif data == '0':
            output = 'east'
        else:
            output = 'error'
        return output

    def GetTrackingStatus(self):
        data_rate = self.send(MNT_GETTRACKINGRATE)[0].split(',')
        data_is_tracking = self.send(MNT_ISTRACKING)[0]
        if int(data_is_tracking) == 1:
            data_is_tracking = 'true'
        else:
            data_is_tracking = 'false'
        output = {
            'is_tracking': data_is_tracking,
            'tracking_rate_Ra': data_rate[0],
            'tracking_rate_Dec': data_rate[1]
        }
        #print(output)
        return output

    def IsSlewComplete(self):
        data = self.send(MNT_ISSLEWCOMPLETE)
        #data = tsx_rational_errors(data)

        # treating this as slew status, true = slewing
        # Is it doing it or not, not is it done doing it. Inconsistencies!!
        if int(data[0]) == 1:
            data = 'false'
        else:
            data = 'true'
        output = { 'slew': data }
        #print(output)
        return output

    def GetStatus(self):
        status_connection = self.IsConnected()
        #print(status_connection['connected'])
        if status_connection['connected'] != 'true':
            output = {
                'Polltime': time.ctime(),
                'Error': 'Error',
                'Connected': status_connection,
                'Parked': '',
                'Slewing': '',
                'Tracking': '',
                'AzAlt': '',
                'RaDec': ''
            }
            return output
        else:
            status_parked = self.IsParked()
            status_sideofpier = self.OTASideOfPier()
            status_slewing = self.IsSlewComplete()
            status_tracking = self.GetTrackingStatus()
            status_AzAlt = self.GetAzAlt()
            status_RaDec = self.GetRaDec()
            status_ObjName = self.GetObjInfoName()
            output = {
                'Polltime': {
                    'epoch': time.time(),
                    'ctime': time.ctime()
                },
                'Connected': status_connection,
                'Parked': status_parked,
                'OTAPierSide': status_sideofpier,
                'Slewing': status_slewing,
                'Tracking': status_tracking,
                'AzAlt': status_AzAlt,
                'RaDec': status_RaDec,
                'Object': status_ObjName
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

class tsxControl():
    def __init__(self, IP_ADDR='127.0.0.1', TCP_PORT=3040, READBUF=4096, output=''):
        self.IP_ADDR = IP_ADDR
        self.TCP_PORT = TCP_PORT
        self.READBUF = READBUF
        self.output = output
        self.socket = socket.create_connection((self.IP_ADDR, self.TCP_PORT))
        self.send(TSX_APPBUILD)
        if (self.recv()[2] != 0):
            raise ValueError('Error reading TSX state')
        self.send(CAM_ASYNCHRONOUS_ON)
        if (self.recv()[2] != 0):
            raise ValueError('Enabling async mode failed!')

    def send(self, CMD):
        self.socket.send((JS_HEADER).encode('utf8'))
        # TODO - allow handling lists in CMD
        self.socket.send((CMD).encode('utf8'))
        self.socket.send((JS_FOOTER).encode('utf8'))

    def recv(self):
        output = ((self.socket.recv(self.READBUF)).decode('utf8')).split('|')
        #print('Debug: %s' % output)
        # Split up TSX output so you get the result, the verbose error, and error code
        # Postitional format:
        # 0 = result (string because I can't guarantee an int is always returned. Handle this downstream.)
        # 1 = verbose error (string)
        # 2 = error code (int)
        output = (str(output[0]), str(output[1].split('.')[0]), int((output[1].split('.')[1]).split('=')[1]))
        return output

class camera(tsxControl):

    def GetTempStatus(self):
        # get current temp
        self.send(CAM_GETCURRENTTEMP)
        temp_current = self.recv()

        # get set point
        self.send(CAM_GETTEMPSETPOINT)
        temp_setpoint = self.recv()

        # get TEC power utilization
        self.send(CAM_GETTECPOWERUTIL)
        tec_powerutil = self.recv()

        output = (temp_current[0],temp_setpoint[0],tec_powerutil[0])
        return(output)

    def GetStatus(self):
        # Things we want in this:
        # Is the camera connected? If not, connect. Except on failure to do so.
        self.send(CAM_CONNECT)
        print(self.recv())
        # What binning is set?
        # What is the temperature?
        self.GetTempStatus()
        # What is it doing right now?
        # Is the filterwheel connected?
        # What filter are we on?

        return(output)

    def AtFocus3(self):
        self.send(CAM_ATFOCUS3)
        output = self.recv()
        return(output)


    #TODO - move these to generic functions outside of the class so they can be reused



def tsx_rational_errors(tsx_result):

    # [0] of the return has the result of the command
    # [1] has the result of the script
    # We may need to know context to know which side to look at
    # TODO - map things as appropriate
    # TODO - reference http://www.bisque.com/x2standard/sberrorx_8h_source.html

    #print('TSX Result is %s // %s' % (tsx_result[0], tsx_result[1]))
    output = tsx_result
    return output

## Here be the base commands from tsx

JS_HEADER = '/* Java Script */\n/* Socket Start Packet */\n'
JS_FOOTER = '\n/* Socket End Packet */\n'
MNT_PREAMBLE = 'sky6RASCOMTele'
THESKY_PREAMBLE = 'sky6RASCOMTheSky'
CAM_PREAMBLE = 'ccdsoftCamera'

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
MNT_OBJINFO_NAME = 'sky6ObjectInformation.Property(0); Out = sky6ObjectInformation.ObjInfoPropOut;'
MNT_SIDEOFPIER = '%s.DoCommand(11,""); Out = %s.DoCommandOutput;' % (MNT_PREAMBLE, MNT_PREAMBLE)

## CAMERA CONTROL CONSTANTS

CAM_ASYNCHRONOUS_ON = '%s.Asynchronous = 1' % CAM_PREAMBLE
CAM_ASYNCHRONOUS_OFF = '%s.Asynchronous = 0' % CAM_PREAMBLE
CAM_ASYNCHRONOUS = '%s.Asynchronous' % CAM_PREAMBLE
CAM_CONNECT = '%s.Connect()' % CAM_PREAMBLE
CAM_STATE = '%s.State' % CAM_PREAMBLE
CAM_GETCURRENTTEMP = '%s.Temperature' % CAM_PREAMBLE
CAM_GETTEMPSETPOINT = '%s.TemperatureSetPoint' % CAM_PREAMBLE
CAM_GETTECPOWERUTIL = '%s.ThermalElectricCoolerPower' % CAM_PREAMBLE
CAM_ATFOCUS3 = '%s.AtFocus3(3,true);' % CAM_PREAMBLE