import os

nmap_location = "nmap"

class NmapHelper:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_results(self):
        command = nmap_location + " -p" + self.port + " -Pn -oG - " + self.ip + "| awk '/open/{print $2}'"
        res = os.popen(command).read()
        # split the string with new line and delete the last one
        res = res.split('\n')
        res = res[:-1]
        print res

test = NmapHelper('192.168.0.0/24', '22')
test.get_results()
