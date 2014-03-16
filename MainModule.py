import sys
sys.path.insert(0, './modules/DiscoveryModule')
sys.path.insert(0, './modules/FingerprintingModule')
sys.path.insert(0, './modules/MaintenanceModule')
sys.path.insert(0, './modules/OffensiveModule')
sys.path.insert(0, './modules/UtilsModule')
sys.path.insert(0, './common/')

from Interface import *
from HostDiscoveryModule import *
from InterfacesRetriever import *
from InternetChecker import *

internet_checker = InternetChecker()
if (internet_checker.check_internet()):
    print "[+] Internet seems to be working."

interfaces = InterfacesRetriever().get_up_interfaces()
if (len(interfaces) > 0):
    print "[+] Seems that there are some up interface(s)"
#for interface in interfaces:
#    host_discovery = HostDiscoveryModule(range_ip)
#    res = host_discovery.execute()
#    print res
discovery = HostDiscoveryModule()
discovery.feed(interfaces)
discovery.execute()
hosts = discovery.getResults()
