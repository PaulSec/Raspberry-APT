import sys
sys.path.insert(0, '../../common/')

import subprocess
import re
from Target import *
from OffensiveModule import OffensiveModule


class HydraModule(OffensiveModule):

    hydra_location = "hydra"
    user_file_location = ""
    pass_file_location = ""

    def loadConfig(self, config):
        if "hydra_location" in config:
            self.hydra_location = config["hydra_location"]
        if "pass_file_location" in config:
            self.pass_file_location = config["pass_file_location"]
        if "user_file_location" in config:
            self.user_file_location = config["user_file_location"]

    def execute(self):
        res = list()
        for target in super(HydraModule, self).getTargets():
            args = [self.hydra_location,
                    target.ip,
                    target.protocol,
                    "-s", target.port,
                    "-P", self.pass_file_location,
                    "-L", self.user_file_location,
                    "-e", "ns",
                    "-t", "10"]
            print args

            hydra = subprocess.Popen(args,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            out, err = hydra.communicate()

            pattern = r"login: ([\w]+) \s+password: ([\w]+)"
            logins = re.findall(pattern, out)
            for login in logins:
                res.append({"protocol": protocol,
                            "ip": target.ip,
                            "port": target.port,
                            "user": login[0],
                            "pass": login[1]})

        super(HydraModule, self).addResult(res)
        super(HydraModule, self).clearTargets()
