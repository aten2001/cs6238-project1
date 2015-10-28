"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: login.py
Object Functions: getParser, createUser, getUser, storeUser, main
Object Description:  The login object is the primary object of the hardened password program.  The login function performs the
                     authentication of user and also manages user accounts.
"""

import User
import helpers
import argparse
import getpass
import shelve
import pickle
import Config
import os
import Crypto.Util.number
import Crypto.Random.random

config = Config.getConfig()

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "data")
SHELF_FILE = os.path.join(BASE_PATH, "passwddb")

#Function getParser() creates an argument parser.
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

#Function createUser(Username) instantiates a user given a username and password
def createUser(username=None, password=None):
    if username == None:
        username = raw_input("Username: ")
    if password == None:
        password = getpass.getpass()
    user = User.User(username, password)

    return user

#Function getUser(username) retrieves a user object given a username
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

#Function storeUser(user) manages the storage of the user object in file storage.
def storeUser(user):
    shelf = shelve.open(SHELF_FILE, writeback=True)

    if not shelf.has_key("users"):
        shelf["users"] = {}
    # Encrypt the history file for storage
    hist = user.historyfile.encrypt()
    # Pick a new 160bit prime
    user.q = Crypto.Util.number.getPrime(160)
    # Create a polynomial with f(0) = hpwd
    user.polynomial = user.genPolynomial()
    # Create an instruction table
    user.instructiontable = user.genInstructionTable()
    # Clear the historyfile, hpwd, and password in preparation
    # for user storage
    user.HistoryFile = None
    #user.hpwd = None
    user.password = None
    shelf["users"][user.username] = (pickle.dumps(user), hist)

    shelf.close()

#Function main() is the main function of the hardened password program
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
                    features = map(int, features.split(","))
                    logins.append((password, features))
            # For each pw and feature array try to authenticate
            for login in logins:
                password = login[0]
                features = login[1]
                user, enc_history = getUser(args["user"])
                if user == None:
                    user = createUser(args["user"])
                    storeUser(user)
                user.password = password
                login = user.deriveHpwd(features)
                if login:
                    user.historyfile = user.getHistoryFile(enc_history)
                    print 1
                    user.historyfile.addEntry(features)
                    storeUser(user)
                else:
                    print 0
        else:
            print "Must specify login file name"
