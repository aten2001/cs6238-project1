"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: HistoryFile.py
Object Functions: tokenFromPassword, addEntry, encrypt, decrypt
Object Description:  The purpose of this object is to instantiate and manage a history containing a set of previous instruction tables.
                     The purpose of the history file is to allow for the final authentication check using the Hpwd as well as to calculate mean and std. deviation of
                     typing features.
"""

import base64
import os
import pickle
import Config
import cryptography
import helpers
from collections import deque
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from PasswordError import PasswordError

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")

config = Config.getConfig()

class HistoryFile(object):
    
    #Object initialization function.  Takes in the hardened password (Hpwd) and a hash function salt as inputs and instantiates the History file
    def __init__(self, password, salt, history=None):
        self.password = password
        self.salt = salt
        self.token = self.tokenFromPassword()
        
        if history == None:
            self.history = deque([])
        else:
            try:
                self.history = self.decrypt(history)
            except cryptography.fernet.InvalidToken:
                raise PasswordError("Incorrect Password")
    
    #Function tokenFromPassword(), hashes the user password using the provided salt and the SHA256 hash function            
    def tokenFromPassword(self):
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=default_backend()
              )
        token = base64.urlsafe_b64encode(
                  kdf.derive(helpers.long_to_bytes(self.password)))
        return token
        
    #Function addEntry(featureArray), accepts an instruction table array and appends it to the existing history file
    def addEntry(self, featureArray):
        length = config.get("historyfile", "length")
        if len(self.history) >= length:     #If the history file is at maximum capacity, remove the oldest entry 
            for i in range(0, (len(self.history) - length) + 1):
                temp = self.history.popleft()
        self.history.append(featureArray)

    #Function encrypt(), takes the history file and encrypts the file using the Fernet symmetric key encryption algorithm and the token generated from Hpwd
    def encrypt(self):
        pickledQueue = pickle.dumps(self.history)
        padLen = config.get("historyfile", "padlength")
        pickledQueue += os.urandom(padLen - len(pickledQueue))
        fern = Fernet(self.token)
        cipher = fern.encrypt(pickledQueue)
        return cipher
    
    #Function decrypt(), takes an encrypted history file and decrypts the file using the token generated from Hpwd
    def decrypt(self, history):
        fern = Fernet(self.token)
        plaintext = fern.decrypt(history)
        queue = pickle.loads(plaintext)
        return queue
