import base64
import os
import pickle
import Config
import cryptography
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

    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt
        self.token = self.tokenFromPassword()
        self.history = self.read()
    
    def tokenFromPassword(self):
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=default_backend()
              )
        token = base64.urlsafe_b64encode(kdf.derive(self.password))
        return token

    def addEntry(self, featureArray):
        length = config.get("historyfile", "length")
        if len(self.history) >= length:
            for i in range(0, (len(self.history) - length) + 1):
                temp = self.history.popleft()
        self.history.append(featureArray)
        self.write(self.history)

    def read(self):
        # Read in file if exists
        HISTFILE = os.path.join(BASE_PATH, self.username)
        if os.path.isfile(HISTFILE):
            with open(HISTFILE, "rb") as f:
                # Decrypt file w/ password
                fern = Fernet(self.token)
                cipher = f.read()
                plaintext = fern.decrypt(cipher)
                # TODO: Unpad file
                # Unpickle array
                queue = pickle.loads(plaintext)
                # Return array
                return queue
        else:
            return deque([])

    def write(self, queue):
        # Pickle the queue
        pickledQueue = pickle.dumps(queue)
        # TODO: Pad queue
        # Encrypt queue w/ password
        fern = Fernet(self.token)
        cipher = fern.encrypt(pickledQueue)
        # Write to file
        with open(os.path.join(BASE_PATH, self.username), "wb") as f:
            f.write(cipher)
