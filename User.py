import Crypto.Util.number
import Crypto.Random.random
import os
import helpers
import HistoryFile
import InstructionTable
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
        self.instructiontable = InstructionTable.InstructionTable(
                                    self.polynomial,
                                    self.q,
                                    self.password)

    def getHistoryFile(self, blob=None):
        if blob == None:
            return HistoryFile.HistoryFile(self.hpwd, self.salt)
        else:
            return HistoryFile.HistoryFile(self.hpwd, self.salt, blob)

    def genPolynomial(self):
        degree = int(config.get("general", "features")) - 1
        a = [self.hpwd]
        for i in range(0, degree):
            a.append(Crypto.Random.random.randint(1, self.q))
        return a

    def deriveHpwd(self, featureArray):
        backend = default_backend()
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=backend
              )

        G = long(kdf.derive(self.password).encode('hex'),16)

        ti = int(config.get("general", "ti"))
        points = []
        i = 0
        for feature in featureArray:
            if feature < ti:
                points.append([self.instructiontable[i][0] * 2,
                               self.instructiontable[i][1] - G % q])
            else:
                points.append([self.instructiontable[i][0] * 2 + 1,
                               self.instructiontable[i][2] - G % q])
        hpwd = helpers.modular_lagrange_interpolation(0, points, self.q)
        return hpwd
