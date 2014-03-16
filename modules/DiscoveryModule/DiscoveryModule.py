from abc import ABCMeta, abstractmethod


class DiscoveryModule(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.ifs = []
        self.hosts = []

    @abstractmethod
    def execute(self):
        pass

    def getIfs(self):
        return self.ifs

    def addHost(self, host):
        self.hosts.append(host)

    def addHosts(self, hosts):
        self.hosts.extend(hosts)

    def getResults(self):
        return self.hosts

    def feed(self, ifs):
        self.ifs.extend(ifs)

    def clearIfs(self):
        self.ifs = []
