import shelve

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")

class HistoryFile(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.historyFile = self.getHistoryFile()
    
    def encrypt(self, password):
        pass

    def decrypt(self, password):
        pass

    def getHistoryFile(self):
        shelf = shelve.open(os.path.join(BASE_PATH, self.username,
                    writeback=True))
        try:
            featurearray = shelf["featurearray"]
        except KeyError:
            shelf["featurearray"] = []


    def addEntry(self, featureArray):
        # Check if 5 entries
        ## If not add entry
        ## Else remove first entry; add entry
        pass
