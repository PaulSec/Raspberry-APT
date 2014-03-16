import sys
sys.path.insert(0, './../UtilsModule')
sys.path.insert(0, './../../common')
from NmapHelper import *
from FingerPrintingModule import *
from Target import *
import re


class NmapVerticalScanModule(NmapHelper, FingerPrintingModule):

    def loadConfig(self, config):
        if "nmap_location" in config:
            self.nmap_location = config["nmap_location"]

    def execute(self):
        for host in super(NmapVerticalScanModule, self).getHosts():
            command = " -Pn -oG - " + host.ip
            res = super(NmapVerticalScanModule, self).execute(command, False)

            pattern = r"(([0-9]+)/open/tcp//([\w]+))"
            open_ports = re.findall(pattern, res)

            for open_port in open_ports:
                print open_port
                port = open_port[1]
                service = open_port[2]

                target = Target(host.ip, port, service)
                super(NmapVerticalScanModule, self).addTarget(target)

