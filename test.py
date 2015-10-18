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
import login

def main():
    print "Creating user..."
    user = login.createUser("kyle", "CorrectPassword")
    print "hpwd:  {0}".format(user.hpwd)
    table = user.instructiontable.generateTable()
    print table

    print "Teting history file encryption:"
    enc_history = user.historyfile.encrypt()
    print enc_history
    print "Testing history file decryption (with original hpwd):"
    dec_history = user.getHistoryFile(enc_history)
    print dec_history

    backend = default_backend()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=user.salt,iterations=10000,backend=backend)
    G = long(kdf.derive(user.password).encode('hex'),16)
    ti = 10
    i = 0

    points = []
    features = [18,10,-2,20,10,4,2,8,6,17,23,20,27,7]

    for feature in features:
      if feature < 10:
        points.append([table[i][0] * 2,table[i][1]])
      else:
        points.append([table[i][0] * 2 + 1, table[i][2]])
      i += 1

    print "Getting points from features {0}".format(features)
    print points

    print "Trying to generate hpwd'..."
    print "hpwd\': {0}".format(helpers.modular_lagrange_interpolation(0, points, user.q))

    print "Adding login features to history file"
    user.historyfile.addEntry(features)

if __name__ == "__main__":
    main()
