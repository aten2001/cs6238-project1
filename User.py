"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: User.py
Object Functions: getHistoryFile, genPolynomial, deriveHpwd
Object Description:  The purpose of this object is to instantiate and manage a user given a username and password.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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

    #Initiate User object give inputs username and password
    def __init__(self, username, password):
        self.username = username
        self.q = Crypto.Util.number.getPrime(160)
        self.hpwd = Crypto.Random.random.randint(1, self.q)
        self.salt = os.urandom(16)
        self.password = password # TODO: hash this
        self.historyfile = self.getHistoryFile()
        self.polynomial = self.genPolynomial()
        self.instructiontable = self.genInstructionTable()

    # Function genInstructioTable() generates a new instruction table from
    # locally stored variables
    def genInstructionTable(self):
        return InstructionTable.InstructionTable(
                self.polynomial, self.q, self.password,
                self.salt, self.historyfile.history)

    #Function getHistoryFile(blob) takes in a history file if one is available and returns a valid history file
    def getHistoryFile(self, blob=None):
        if blob == None:
            return HistoryFile.HistoryFile(self.hpwd, self.salt)
        else:
            return HistoryFile.HistoryFile(self.hpwd, self.salt, history=blob)

    #Function genPolynomial() accepts no inputs and will generate and return a polynomial which will be used
    def genPolynomial(self):
        degree = int(config.get("general", "features")) - 1
        a = [self.hpwd]
        for i in range(0, degree):
            a.append(Crypto.Random.random.randint(1, self.q))
        return a

    #Function deriveHpwd(featureArray) accepts an array of typing features associated with a password and derives Hpwd from
    #the instruction table
    def deriveHpwd(self, featureArray):
        table = self.instructiontable.generateTable()
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
        errorcorrect = []
        i = 0
        for feature in featureArray:
            if int(feature) < ti:
                points.append([table[i][0] * 2,
                               table[i][1] - G % self.q])
            else:
                points.append([table[i][0] * 2 + 1,
                               table[i][2] - G % self.q])
            i += 1

        i = 0
        for point in points:
            errorcorrect.append(points)
            if point[0] % 2 == 0:
                errorcorrect[i][0] = table[i][0] * 2 + 1
                errorcorrect[i][1] = table[i][2] - G % self.q
            else:
                errorcorrect[i][0] = table[i][0] * 2
                errorcorrect[i][1] = table[i][1] - G % self.q
            i += 1

        hpwd = helpers.modular_lagrange_interpolation(0, points, self.q)

        # Create an array with point arrays with one feature changed
        hpwdAlternates = []
        for points in errorcorrect:
            hpwdAlternates.append(helpers.modular_lagrange_interpolation(0, points, self.q))

        return hpwd, hpwdAlternates
