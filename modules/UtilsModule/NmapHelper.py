import os

from Host import *

nmap_location = "nmap"


class NmapHelper(object):

    def execute(self, command, grepable=False):
        command = nmap_location + command
        out = os.popen(command).read()
        # split the string with new line and delete the last one
        res = []
        if (grepable):
            out = out.split('\n')
            out = out[:-1]
            for ip in out:
                res.append(Host(ip))
        return res
