# found on <http://code.activestate.com/recipes/439093/#c1>

import socket
import fcntl
import struct
import array


class InterfacesRetriever(object):
    """
        Internet Checker Main CLass
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(InterfacesRetriever, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def all_interfaces(self):
        max_possible = 128  # arbitrary. raise if needed.
        bytes = max_possible * 32
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', '\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        namestr = names.tostring()
        lst = []
        for i in range(0, outbytes, 40):
            name = namestr[i:i + 16].split('\0', 1)[0]
            ip = namestr[i + 20:i + 24]
            lst.append((name, ip))
        return lst

    def format_ip(self, addr):
        return str(ord(addr[0])) + '.' + \
            str(ord(addr[1])) + '.' + \
            str(ord(addr[2])) + '.' + \
            str(ord(addr[3]))

    def get_up_interfaces(self):
        ifs = self.all_interfaces()
        res = {}
        for i in ifs:
            res[i[0]] = self.format_ip(i[1])

        # deleting localhost (lo interface)
        try:
            del res['lo']
        except:
            pass
        return res
