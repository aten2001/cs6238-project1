import Crypto.Util.number
import random

class User(object):

    def __init__(self, username):
        self.username = username
        self.q = Crypto.Util.number.getPrime(160)
        self.h = 4
        self.hpwd = random.randint(1, self.q)
