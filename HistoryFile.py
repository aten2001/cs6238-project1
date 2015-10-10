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

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")

config = Config.getConfig()

class HistoryFile(object):

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
                # TODO: raise error
                return None

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

    def addEntry(self, featureArray):
        length = config.get("historyfile", "length")
        if len(self.history) >= length:
            for i in range(0, (len(self.history) - length) + 1):
                temp = self.history.popleft()
        self.history.append(featureArray)

    def encrypt(self):
        pickledQueue = pickle.dumps(self.history)
        # TODO: pad queue
        fern = Fernet(self.token)
        cipher = fern.encrypt(pickledQueue)
        return cipher

    def decrypt(self, history):
        fern = Fernet(self.token)
        plaintext = fern.decrypt(history)
        queue = pickle.loads(plaintext)
        return queue
