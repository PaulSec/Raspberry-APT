from abc import ABCMeta, abstractmethod


class OffensiveModule(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.targets = []
        self.results = []

    @abstractmethod
    def execute(self):
        pass

    def getTargets(self):
        return self.targets

    def addResult(self, result):
        self.results.append(result)

    def addResults(self, results):
        self.results.extend(results)

    def getResults(self):
        return self.results

    def feed(self, targets):
        self.targets.extend(targets)

    def clearTargets(self):
        self.targets = []
