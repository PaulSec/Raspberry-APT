import sys
sys.path.insert(0, './../UtilsModule')
sys.path.insert(0, './../../common')
from NmapHelper import *
from FingerPrintingModule import *
from Target import *


class NmapHorizontalScanModule(NmapHelper, FingerPrintingModule):

    port = ""

    def loadConfig(self, config):
        if "port" in config:
            self.port = config["port"]
        if "nmap_location" in config:
            self.nmap_location = config["nmap_location"]

    def execute(self):
        for host in super(NmapHorizontalScanModule, self).getHosts():
            command = " -p" + self.port
            command += " -Pn -oG - "
            command += host.ip + " |awk '/open/{print $2, $5}'"

            res_command = super(NmapHorizontalScanModule, self).execute(command, True)
            res_command = ''.join(res_command)
            if (len(res_command) > 0):
                res_command = res_command.split(' ')[1]
                port = res_command.split('//')[0]
                port = port.split('/')[0]
                service = res_command.split('//')[1]
                target = Target(host.ip, port, service)
                super(NmapHorizontalScanModule, self).addTarget(target)

    def setPort(self, port):
        self.port = port
