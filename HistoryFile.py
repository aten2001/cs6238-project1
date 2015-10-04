import shelve
import Config
from collections import deque

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")

config = Config.getConfig()

class HistoryFile(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.history = self.getHistory()
    
    def encrypt(self, featurearray):
        # TODO: encrypt with password
        return featurearray

    def decrypt(self, featurearray):
        # TODO: decrypt with password
        return featurearray

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
