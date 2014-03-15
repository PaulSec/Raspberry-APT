import sys
sys.path.insert(0, '../../common/')

import subprocess
import re
from Target import *

''' Module example
targets = [Target("192.168.0.11", "22")]
module = HydraModule()
print module.execute("ssh", targets)
'''


class HydraModule:

    def __init__(self, hydra_path="hydra", login_dict="/tmp/users.txt", pass_dict="/tmp/pass.txt"):
        self.hydra_path = hydra_path
        self.login_dict = login_dict
        self.pass_dict = pass_dict

    def execute(self, protocol, targets):
        res = list()
        for target in targets:
            args = [self.hydra_path, target.ip, protocol, "-s", target.port, "-P", self.pass_dict, "-L", self.login_dict, "-e", "ns", "-t", "10"]
            print args

            hydra = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = hydra.communicate()

            pattern = r"login: ([\w]+) \s+password: ([\w]+)"
            logins = re.findall(pattern, out)
            for login in logins:
                res.append({"protocol": protocol, "ip": target.ip, "port": target.port, "user": login[0], "pass": login[1]})
        return res
