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
    if file_path is not None:
        module = importlib.import_module(module_name)
        return getattr(module, module_name)
    print "Cannot find %s.py" % module_name
    return None


def parse_workflows(file_name):
    flowname_regexp = r"\[WF=(\w+)\]"
    modulename_regexp = r"\[MODULE=(\w+)\]"
    flows = {}
    configs = {}
    parsingName = ""
    parsingType = ""

    for line in open(file_name).read().splitlines():
        if parsingType == "" or parsingType == "module":
            #Parsing flow name
            regexWf = re.search(flowname_regexp, line)
            if regexWf is not None:
                parsingName = regexWf.group(1)
                parsingType = "wf"
                continue
            else:
                regexModule = re.search(modulename_regexp, line)
                if regexModule is not None:
                    parsingName = regexModule.group(1)
                    parsingType = "module"
                    configs[parsingName] = {}
                    continue
                elif parsingType == "":
                    print "Expected begining of a flow or a module configuration, found %s" % line
                    return None
        if parsingType == "wf":
            #Parsing flow
            modulenames = line.split("->")
            modules = []
            for modulename in modulenames:
                module = load_module(modulename)
                if module is None:
                    print "Cannot load module: %s for workflow %s" % (modulename, parsingName)
                    return None
                modules.append((modulename, module))
            if len(modules) != 3:
                print "Expected three modules when parsing %s. See doc for more info." % parsingName
                return None
            flows[parsingName] = modules
            parsingType = ""
        elif parsingType == "module":
            tokens = line.split(":")
            if len(tokens) != 2:
                print "Expected a definition for module %s, found %s." % (parsingName, line)
                return None
            configs[parsingName][tokens[0]] = tokens[1]

    return flows, configs

if len(sys.argv) != 2:
    print "Usage is %s <config file>" % sys.argv[0]
    sys.exit(0)

cfg_file_name = sys.argv[1]
if not os.path.isfile(cfg_file_name):
    print "Cannot find the specified configuration file: %s" % cfg_file_name

flows, configs = parse_workflows(cfg_file_name)

if flows is None:
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
    for modulename, module in flow:
        instance = module()
        if modulename in configs:
            instance.loadConfig(configs[modulename])
        instance.feed(moduleResults)
        instance.execute()
        moduleResults = instance.getResults()
