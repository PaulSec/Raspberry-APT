import os
import sys
sys.path.insert(0, '../../common/')
from Host import *


class NmapHelper(object):

    nmap_location = "nmap"

    def execute(self, command, grepable=False):
        command = self.nmap_location + command
        print command
        res = os.popen(command).read()
        # split the string with new line and delete the last one
        if (grepable):
            res = res.split('\n')
            res = res[:-1]
        return res
