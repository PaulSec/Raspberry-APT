from abc import ABCMeta, abstractmethod


class DiscoveryModule(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.interfaces = []
        self.hosts = []

    @abstractmethod
    def execute(self):
        pass

    def getInterfaces(self):
        return self.interfaces

    def addHost(self, host):
        self.hosts.append(host)

    def addHosts(self, hosts):
        self.hosts.extend(hosts)

    def getResults(self):
        return self.hosts

    def feed(self, interfaces):
        self.interfaces.extend(interfaces)

    def clearInterfaces(self):
        self.interfaces = []
