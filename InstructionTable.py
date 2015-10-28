"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: InstructionTable.py
Object Functions: generateTable, polynomial, genAlpha, genBeta, getMean, getStddev 
Object Description:  The purpose of this object is to instantiate and manage an instruction table.  The purpose of the instruction
                     table is to generate polynomial values which contstruct to form a polymial.  If the polynomial is contructed 
                     appropriately based on typing features of the user, the polynomial can be evaluated to determing the Hpwd.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import Crypto.Random.random
import Config
import os
import statistics

config = Config.getConfig()

class InstructionTable(object):
    
    #Object instantiation function which creates an instruction table object.
    def __init__(self, coefficients, q, password, salt, history):
        self.q = q
        self.coefficients = coefficients
        self.password = password
        self.salt = salt
        self.history = history

    #Function generateTable() will generate an instruction table given the inputs provided during the object instantiation
    def generateTable(self):
        degree = int(config.get("general", "features"))
        ti = int(config.get("general", "ti"))
        k = int(config.get("crypto", "k"))
        table = []
        mean = None
        stdev = None
        if len(self.history) >= 5:
            mean = self.getMean()
            stdev = self.getStddev()
        for i in range(1, int(degree) + 1):
            alpha = True 
            beta = True
            if mean != None:
                try:
                    if abs(mean[i] - ti) > k * stdev[i]:
                        beta = False
                    elif abs(mean[i] - ti) < k * stdev[i]:
                        alpha = False
                except IndexError:
                    pass
            table.append([i,
                          alpha,
                          beta])
        return table

    #Function polynomial(base) will generate a polynomial given a base and the coefficients provided during object instantiation
    def polynomial(self, base):
        result = 0
        exponent = 0
        for coefficient in self.coefficients:
            result += coefficient * pow(base, exponent)
            exponent += 1
        return result

    #Function genAlpha(i) will generate an alpha value to be included in the alpha column of an instruction table given the input i
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
        alpha = y #+ G % self.q
        return alpha

    #Function genBeta(i) will generate a beta value to be included in the beta column of an instruction table given the input i
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
        beta = y #+ G % self.q
        return beta
    
    #Function getMean() provides the mean across all columns of the history file provided during object instantiation
    def getMean(self):
        mean = map(lambda x:statistics.mean(x), zip(*self.history))
        return mean

    #Function getStddev() provides the standard deviation across all columns of the history file provided during object instantiation
    def getStddev(self):
        stdev = map(lambda x:statistics.stdev(x), zip(*self.history))
        return stdev
