
"""
This module lets me put all the necessary TSX commands into a separate file.
"""
import socket

class mount(object):

    def __init__(self, IP_ADDR='127.0.0.1', TCP_PORT=3040, READBUF=4096):
        self.IP_ADDR = IP_ADDR
        self.TCP_PORT = TCP_PORT
        self.READBUF = READBUF

    def connect(self):
        # I'm not sure this actually works, socket seems to die immediately
        # so what's the point?
        # TODO - delete this if not necessary!!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.IP_ADDR, self.TCP_PORT))
        return s

    def send(self, CMD):
        # TODO - connection error handling
        # TODO - logging of actions
        # TODO - Sane output
        # TODO - debug level
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.IP_ADDR, self.TCP_PORT))
        print 'Sending %s command...' % CMD
        s.send(bytes('/* Java Script */\n' +
                           '/* Socket Start Packet */\n' + CMD +
                           '\n/* Socket End Packet */\n'))
        print 'Command has been sent!'
        output = s.recv(4096)
        print 'output is %s' % output

    ## START - basic command library

    def tsxcheck(self):
        # make sure TSX is running
        self.send(APPBUILD)
    def parkdnd(self):
        self.send(PARKDND)
    def is_parked(self):
        self.send(IS_PARKED)
    def unpark(self):
        self.send(UNPARK)
    def find_home(self):
        self.send(FIND_HOME)

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

## MOUNT
APPBUILD = 'Application.build'
MNT_PREAMBLE = 'sky6RASCOMTele'
PARK = '%s.Park();' % MNT_PREAMBLE
PARKDND = '%s.ParkAndDoNotDisconnect();' % MNT_PREAMBLE
IS_PARKED = '%s.IsParked();' % MNT_PREAMBLE
UNPARK = '%s.Unpark();' % MNT_PREAMBLE
FIND_HOME = '%s.FindHome();' % MNT_PREAMBLE
