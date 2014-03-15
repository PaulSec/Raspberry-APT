import urllib2


class InternetChecker(object):
    """
        Internet Checker Main CLass
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(InternetChecker, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def check_internet(self):
        try:
            header = {"pragma": "no-cache"}
            req = urllib2.Request("http://www.google.com", headers=header)
            urllib2.urlopen(req, timeout=2)
            return True
        except urllib2.URLError as err:
            print err
