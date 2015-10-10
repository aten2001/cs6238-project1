import User
import argparse
import getpass
import shelve
import pickle
import Config

config = Config.getConfig()

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")
SHELF_FILE = os.path.join(BASE_PATH, "passwddb")

def getParser():
    parser = argparse.ArgumentParser(description = "Login program for \
                                                    hardened password \
                                                    application.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--create', action = store_true, default = False,
                        help = "Create a user.")
    group.add_argument('file', help = "Path to login file.")

    return parser

def createUser():
    username = raw_input("Username: ")
    password = getpass.getpass()
    user = User.User(username, password)

    return user

def getUser(username):
    shelf = shelve.open(SHELF_FILE)

    try:
        user = shelf["users"][username]
    except KeyError:
        user = None
    finally:
        shelf.close()
        return user

def storeUser(user):
    shelf = shelve.open(SHELF_FILE)

    if not shelf.has_key("users"):
        shelf["users"] = {}
    hist = user.HistoryFile.encrypt()
    user.HistoryFile = None
    user.hpwd = None
    shelf["users"][user.username] = (pickle.dumps(user), hist)

    shelf.close()

if __name__ == "__main__":
    parser = getParser()
    args = parser.parse_args()
    args = vars(args)

    if args["create"]:
        user = createUser()
        storeUser(user)

    else:
        with open(args["file"], "r"):
            # Read lines from file
            # For each pw and feature array try to auth
            pass
        pass
