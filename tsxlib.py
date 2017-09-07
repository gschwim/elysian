
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
        self.tsxcheck()
        self.is_parked()
        self.find_home()
        self.parkdnd()
        self.is_parked()


def connect(IP_ADDR='127.0.0.1', TCP_PORT=3040, READBUF=4096):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_ADDR, TCP_PORT))
    return s


## Here be the base commands from tsx

## MOUNT
APPBUILD = 'Application.Build'
MNT_PREAMBLE = 'sky6RASCOMTele'
PARK = '%s.Park();' % MNT_PREAMBLE
PARKDND = '%s.ParkAndDoNotDisconnect();' % MNT_PREAMBLE
IS_PARKED = '%s.IsParked();' % MNT_PREAMBLE
UNPARK = '%s.Unpark();' % MNT_PREAMBLE
FIND_HOME = '%s.FindHome();' % MNT_PREAMBLE








## old command set. Probably don't need these
## TODO - delete these at some point

JS_KEY_START = """
    /* Java Script */
    /* Socket Start Packet */
"""

JS_KEY_END = """
    /* Socket End Packet */
"""

POLL_STATE = """
    %s
    ccdsoftCamera.State
    %s
""" % (JS_KEY_START, JS_KEY_END)

PARK_MOUNT = """
    %s
    ccdsoftAutoguider.Disconnect();
    ccdsoftCamera.Disconnect();
    sky6RASCOMTele.Park();
    %s
""" % (JS_KEY_START, JS_KEY_END)
