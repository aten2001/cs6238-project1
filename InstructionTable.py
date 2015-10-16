from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import Crypto.Random.random
import Config
import os
import statistics

config = Config.getConfig()

class InstructionTable(object):

    def __init__(self, coefficients, q, password, salt, history):
        self.q = q
        self.coefficients = coefficients
        self.password = password
        self.salt = salt
        self.history = history

    def generateTable(self):
        degree = config.get("general", "features")
        ti = config.get("general", "ti")
        table = []
        mean = None
        stdev = None
        if len(self.history) >= 5:
            mean = getMean()
            stdev = getStddev()
        for i in range(1, int(degree) + 1):
            alpha = self.genAlpha(i)
            beta = self.genBeta(i)
            if not mean:
                if math.abs(mean - int(ti)) > k * stdev:
                    beta += Crypto.Random.random.randint(1, self.q) % self.q
                elif math.abs(mean - int(ti)) < k * stdev:
                    alpha += Crypto.Random.random.randint(1, self.q) % self.q
            table.append([i,
                          alpha,
                          beta])
        return table

    def polynomial(self, base):
        result = 0
        exponent = 0
        for coefficient in self.coefficients:
            result += coefficient * pow(base, exponent)
            exponent += 1
        return result

    def genAlpha(self, i):
        backend = default_backend()
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=backend
              )

        y = self.polynomial(2 * i)

        G = long(kdf.derive(self.password).encode('hex'),16)
        alpha = y + G % self.q
        return alpha

    def genBeta(self, i):
        backend = default_backend()
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=backend
              )

        y = self.polynomial(2 * i + 1)

        G = long(kdf.derive(self.password).encode('hex'),16)
        beta = y + G % self.q
        return beta

    def getMean(self):
        mean = map(lambda x:statistics.mean(x), zip(*self.history))
        return mean

    def getStddev(self):
        stdev = map(lambda x:statistics.stdev(x), zip(*self.history))
        return stdev
