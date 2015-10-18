"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: PasswordError.py
Object Functions: PasswordError
Object Description:  The purpose of this class is to implement the PasswordError(Exception) function that defines a password exception.
"""

class PasswordError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
