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
        self.hpwd = Crypto.Random.random.randint(1, self.q) # TODO: don't use random
        self.salt = os.urandom(16)
        self.password = password # TODO: hash this
        self.historyfile = self.getHistoryFile()

    def getHistoryFile(self):
        return HistoryFile.HistoryFile(self.username, self.hpwd, self.salt)

    def saveHistFile(self):
        pass
