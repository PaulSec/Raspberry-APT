import os
import sys
sys.path.insert(0, '../../common/')
from Host import *

nmap_location = "nmap"


class NmapHelper(object):

    def execute(self, command, grepable=False):
        command = nmap_location + command
        print command
        res = os.popen(command).read()
        # split the string with new line and delete the last one
        if (grepable):
            res = res.split('\n')
            res = res[:-1]
        return res
