from abc import ABCMeta, abstractmethod


class FingerPrintingModule(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.hosts = []
        self.targets = []

    @abstractmethod
    def execute(self):
        pass

    def getHosts(self):
        return self.hosts

    def addTarget(self, target):
        self.targets.append(target)

    def addHosts(self, targets):
        self.targets.extend(targets)

    def getResults(self):
        return self.targets

    def feed(self, hosts):
        self.hosts.extend(hosts)

    def clearHosts(self):
        self.hosts = []
