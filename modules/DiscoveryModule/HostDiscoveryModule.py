import sys
from DiscoveryModule import *

sys.path.insert(0, './modules/UtilsModule')
from NmapHelper import *


class HostDiscoveryModule(NmapHelper, DiscoveryModule):

    def loadConfig(self, config):
        if "nmap_location" in config:
            self.nmap_location = config["nmap_location"]

    def execute(self):
        for iface in super(HostDiscoveryModule, self).getInterfaces():
            print "Interface : %s (%s) up." % (iface.ifname, iface.ip)
            range_ip = iface.ip.split('.')
            range_ip[3] = '0/24'
            range_ip = '.'.join(range_ip)
            command = " -sP " + range_ip + " -oG - "
            command = command + "| awk '/Up/{print $2}'"
            hosts = super(HostDiscoveryModule, self).execute(command, True)

            for host in hosts:
                host = Host(host)
                super(HostDiscoveryModule, self).addHost(host)

            super(HostDiscoveryModule, self).clearInterfaces()
