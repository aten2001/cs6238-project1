import Crypto.Util.number
import random
import os
import HistoryFile

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.q = Crypto.Util.number.getPrime(160)
        self.h = 5
        self.hpwd = random.randint(1, self.q)
        self.historyfile = self.getHistoryFile()
        self.passwd = password

    def getHistoryFile(self):
        return HistoryFile(self.username, self.password)

    def saveHistFile(self):
        pass
