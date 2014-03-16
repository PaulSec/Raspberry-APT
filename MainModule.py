import sys
import importlib
import os
import re

sys.path.insert(0, './modules/DiscoveryModule')
sys.path.insert(0, './modules/FingerprintingModule')
sys.path.insert(0, './modules/MaintenanceModule')
sys.path.insert(0, './modules/OffensiveModule')
sys.path.insert(0, './modules/UtilsModule')
sys.path.insert(0, './common/')

from Interface import *
from Host import *
from Target import *
from InterfacesRetriever import *
from InternetChecker import *

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def load_module(module_name):
    file_path = find_file(module_name + ".py", "modules")
    if file_path != None:
        module = importlib.import_module(module_name)
        return getattr(module, module_name)
    print "Cannot find %s.py" % module_name
    return None

def parse_workflows(file_name):
    flowname_regexp = r"\[WF=(\w+)\]"
    flows = {}
    lastflow = ""
    for line in open(file_name).read().splitlines():
        if len(lastflow) == 0:
            #Parsing flow name
            regex = re.search(flowname_regexp, line)
            if regex != None:
                lastflow = regex.group(1)
            else:
                print "Expected begining of a flow, found %s" % line
                return None
        else:
            #Parsing flow
            modulenames = line.split("->")
            modules = []
            for modulename in modulenames:
                module = load_module(modulename)
                if module == None:
                    print "Cannot load module: " + modulename
                    return None
                modules.append(module)
            if len(modules) != 3:
                print "Expected three modules. See doc for more info."
                return None
            flows[lastflow] = modules
            lastflow = ""
    return flows

if len(sys.argv) != 2:
    print "Usage is %s <config file>" % sys.argv[0]
    sys.exit(0)

cfg_file_name = sys.argv[1]
if not os.path.isfile(cfg_file_name):
    print "Cannot find the specified configuration file: %s" % cfg_file_name

flows = parse_workflows(cfg_file_name)

if flows == None:
    exit(0)

print "[+] Config file loaded, %d flows found." % len(flows)

internet_checker = InternetChecker()
if (internet_checker.check_internet()):
    print "[+] Internet seems to be working."

interfaces = InterfacesRetriever().get_up_interfaces()
if (len(interfaces) > 0):
    print "[+] Seems that there are some up interface(s)"

for name, flow in flows.iteritems():
    print "Executing %s" % name
    moduleResults = interfaces
    for module in flow:
        instance = module()
        instance.feed(moduleResults)
        instance.execute()
        moduleResults = instance.getResults()
