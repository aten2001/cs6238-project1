"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: Config.py
Object Functions: getConfig
Object Description:  This function opens the configuration file located at config/default.conf and returns a ConfigParser object
"""

import os
import ConfigParser

def getConfig():
    BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "config")

    try:
        with open(os.path.join(BASE_PATH, "default.conf"), "r") as f:
            parser = ConfigParser.SafeConfigParser()
            parser.readfp(f)
            return parser
    except IOError:
        # TODO: change to raise error about there being no config
        return None
