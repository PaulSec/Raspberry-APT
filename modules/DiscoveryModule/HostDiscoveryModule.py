import sys
sys.path.insert(0, './modules/UtilsModule')
from NmapHelper import *


class HostDiscoveryModule(NmapHelper):

    def __init__(self, range_ip):
        self.range_ip = range_ip

    def execute(self):
        command = " -sP " + self.range_ip + " -oG - "
        command = command + "| awk '/Up/{print $2}'"
        res = super(HostDiscoveryModule, self).execute(command, True)
        # split the string with new line and delete the last one
        return res
