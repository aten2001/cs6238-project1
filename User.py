import Crypto.Util.number
import random
import Config

config = Config.getConfig()

class User(object):

    def __init__(self, username):
        self.username = username
        self.q = Crypto.Util.number.getPrime(160)
        self.h = config.get("historyfile", "length")
        self.hpwd = random.randint(1, self.q)
