import os

nmap_location = "/home/paul/Perso/Hacking/tools/nmap/nmap"


class NmapHelper(object):

    def execute(self, command, grepable=False):
        command = nmap_location + command
        res = os.popen(command).read()
        # split the string with new line and delete the last one
        if (grepable):
            res = res.split('\n')
            res = res[:-1]
        return res

