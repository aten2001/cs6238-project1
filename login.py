import User
import helpers
import argparse
import getpass
import shelve
import pickle
import Config
import os

config = Config.getConfig()

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")
SHELF_FILE = os.path.join(BASE_PATH, "passwddb")

def getParser():
    parser = argparse.ArgumentParser(description = "Login program for \
                                                    hardened password \
                                                    application.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--create', action = 'store_true', default = False,
                        help = "Create a user.")
    group.add_argument('--file', help = "Path to login file.")
    parser.add_argument('--user', '-u', default = "ta", 
                         help = "Name of user to create or login to.")

    return parser

def createUser(username=None):
    if username == None:
        username = raw_input("Username: ")
    password = getpass.getpass()
    user = User.User(username, password)

    return user

def getUser(username):
    shelf = shelve.open(SHELF_FILE)

    try:
        pickled_user, enc_history = shelf["users"][username]
        user = pickle.loads(pickled_user)
        return user, enc_history
    except KeyError:
        return None, None
    finally:
        shelf.close()

def storeUser(user):
    shelf = shelve.open(SHELF_FILE, writeback=True)

    if not shelf.has_key("users"):
        shelf["users"] = {}
    hist = user.historyfile.encrypt()
    user.HistoryFile = None
    user.hpwd = None
    shelf["users"][user.username] = (pickle.dumps(user), hist)

    shelf.close()

if __name__ == "__main__":
    parser = getParser()
    args = parser.parse_args()
    args = vars(args)

    if args["create"]:
        if args["user"]:
            user = createUser(username=args["user"])
        else:
            user = createUser()
        storeUser(user)
    else:
        logins = []
        if args["file"]:
            with open(args["file"], "r") as f:
                for password, features in helpers.read_2_lines(f):
                    logins.append((password, features))
            # For each pw and feature array try to auth
            for login in logins:
                password = login[0]
                features = login[1].split(',')
                user, enc_history = getUser(args["user"])
                if user == None:
                    user = createUser(args["user"])
                    storeUser(user)
                if password != user.password:
                    print "Password ({0}) does not match {1}".format(
                            password, user.password)
                    print 0
                else:
                    user.hpwd = user.deriveHpwd(features)
                    user.historyfile = user.getHistoryFile(enc_history)
                    login = True
                    print "Password matches"
                    if login:
                        user.historyfile.addEntry(features)
                        storeUser(user)
        else:
            print "Must specify login file name"
