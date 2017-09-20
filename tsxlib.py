

################################################################################
## This module will provide the base interactions with The Sky X via the
## TCP server.
##
## It is structured as follows:
##
## - connection function - reusable to the other classes, returns values that are
##   useful for downstream parsing. Each class will rely on this.
##
## - class mount() - this class will provide state information of the mount,
##    as well as allow actions to occur e.g. homing, slewing, parking, etc
##
## - class imager() - this class will handle all things that are relevant to cameras,
##    focusers, rotators, guiders, etc.
##
#################################################################################

import socket

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
            s.connect((self.IP_ADDR, self.TCP_PORT))
            s.send(bytes('/* Java Script */\n' +
                         '/* Socket Start Packet */\n' + CMD +
                         '\n/* Socket End Packet */\n'))
            self.output = s.recv(4096).split('|')
        except:
            self.output = 'Error!'
            return self.output
        else:
            return self.output


    ## START - basic command library

    def tsxcheck(self):
        output = self.send(APPBUILD)
        return self.output

    def parkdnd(self):
        output = self.send(PARKDND)
        return self.output

    def is_parked(self):
        output = self.send(IS_PARKED)
        return self.output

    def unpark(self):
        output = self.send(UNPARK)
        return self.output

    def find_home(self):
        output = self.send(FIND_HOME)
        return self.output

    ## END - basic command library

    def park_safely(self):
        # 'Safely' is subjective
        # This command will do the following as a "safe" park
        # 1) tsxcheck() - verify TSX is running
        # 2) is_parked() - see if the mount is parked first
        # 3) find_home() - this make sure we know where we are
        # 4) parkdnd() - park and don't disconnect.
        # 5) is_parked() - see if we're parked again.

        # TODO - trap on TSX not being up
        self.tsxcheck()
        # TODO - if parked, do we really want to home?
        # TODO - verify that parked and appropriate absolute position match
        self.is_parked()
        # TODO - would be nice to know for certain that we're homed
        # - might need an ask to Bisque
        self.find_home()
        self.parkdnd()
        # TODO - throw an exception if it does not show parked
        # TODO - verify absolute position as above
        self.is_parked()

## Here be the base commands from tsx


APPBUILD = 'Application.build'

## MOUNT

MNT_PREAMBLE = 'sky6RASCOMTele'
PARK = '%s.Park();' % MNT_PREAMBLE
PARKDND = '%s.ParkAndDoNotDisconnect();' % MNT_PREAMBLE
IS_PARKED = '%s.IsParked();' % MNT_PREAMBLE
UNPARK = '%s.Unpark();' % MNT_PREAMBLE
FIND_HOME = '%s.FindHome();' % MNT_PREAMBLE
