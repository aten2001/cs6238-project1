import Crypto.Util.number
import Crypto.Random.random
import os
import HistoryFile
import Config

config = Config.getConfig()

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.q = Crypto.Util.number.getPrime(160)
        self.hpwd = Crypto.Random.random.randint(1, self.q)
        self.salt = os.urandom(16)
        self.password = password # TODO: hash this
        self.historyfile = self.getHistoryFile()
        self.polynomial = self.genPolynomial()

    def getHistoryFile(self):
        return HistoryFile.HistoryFile(self.username, self.hpwd, self.salt)

    def saveHistFile(self):
        pass

    def genPolynomial(self):
        degree = config.get("general", "features") - 1
        a = [self.hpwd]
        for i in range(0, degree):
            a.append(Crypto.Random.random.randint(1, self.q))
        return a
