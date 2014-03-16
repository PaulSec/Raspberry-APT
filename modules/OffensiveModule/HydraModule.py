import sys
sys.path.insert(0, '../../common/')

import subprocess
import re
from Target import *
from OffensiveModule import OffensiveModule

hydra_path = "hydra"


class HydraModule(OffensiveModule):
    def execute(self):
        res = list()
        for target in super(HydraModule, self).getTargets():
            args = [hydra_path,
                    target.ip,
                    target.protocol,
                    "-s", target.port,
                    "-P", "/tmp/pass.txt",
                    "-L", "/tmp/usrs.txt",
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
