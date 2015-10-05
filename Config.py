import os
import ConfigParser

def getConfig():
    BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "config")

    try:
        with open(os.path.join(BASE_PATH, "default.conf")) as f:
            parser = ConfigParser.SafeConfigParser()
            parser.read(f)
            return parser
    except IOError:
        # TODO: change to raise error about there being no config
        return None
