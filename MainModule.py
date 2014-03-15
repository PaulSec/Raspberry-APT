import sys
sys.path.insert(0, './modules/DiscoveryModule')
sys.path.insert(0, './modules/FingerprintingModule')
sys.path.insert(0, './modules/MaintenanceModule')
sys.path.insert(0, './modules/OffensiveModule')
sys.path.insert(0, './modules/UtilsModule')

from HostDiscoveryModule import *
from InterfacesRetriever import *
from InternetChecker import *

internet_checker = InternetChecker()
if (internet_checker.check_internet()):
    print "[+] Internet seems to be working."

interfaces = InterfacesRetriever().get_up_interfaces()
if (len(interfaces) > 0):
    print "[+] Seems that there are some up interface(s)"
for interface in interfaces:
    print "Interface : %s (%s) up." % (interface, interfaces[interface])
    range_ip = interfaces[interface].split('.')
    range_ip[3] = '0/24'
    range_ip = '.'.join(range_ip)
    host_discovery = HostDiscoveryModule(range_ip)
    host_discovery.execute()
