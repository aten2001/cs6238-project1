import base64
import os
import shelve
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
        self.token = tokenFromPassword(self)
        self.salt = salt
        self.history = self.getHistory()
    
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

    def encrypt(self):
        # TODO: encrypt with password
        pass

    def decrypt(self):
        # TODO: decrypt with password
        pass

    def getHistory(self):
        shelf = shelve.open(os.path.join(BASE_PATH, self.username))
        try:
            history = shelf["history"]
        except KeyError:
            history = []
        finally:
            shelf.close()
            return history

    def addEntry(self, featureArray):
        length = config.get("historyfile", "length")
        shelf = shelve.open(os.path.join(BASE_PATH, self.username))
        try:
            history = shelf["history"]
        except KeyError:
            history = deque([])
        finally:
            if len(history) < length:
                history.append(self.encrypt(featureArray))
            else:
                for i in range(0, (len(history) - length) + 1):
                    temp = queue.popleft()
                history.append(self.encrypt(featureArray))
                shelf["history"] = history

    def open(self):
        # Read in file
        with open(os.path.join(BASE_PATH, self.username)) as f:
            # Decrypt file w/ password
            fern = Fernet(self.token)
            cipher = f.read()
            plaintext = fern.decrypt(cipher)
            # TODO: Unpad file
            # Unpickle array
            # Return array

    def write(self, array):
        # Pickle array
        # Pad array
        # Encrypt array w/ password
        # Write to file
        pass
