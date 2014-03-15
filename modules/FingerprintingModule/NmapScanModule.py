import sys
sys.path.insert(0, './../UtilsModule')
from NmapHelper import *


class NmapScanModule(NmapHelper):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def execute(self):
        command = " -p" + self.port
        command = command + " -Pn -oG - " + self.ip + "|awk '/open/{print $2}'"
        res = super(NmapScanModule, self).execute(command, True)
        # split the string with new line and delete the last one
        print res
