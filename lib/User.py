#!/usr/bin/python

from lib.Role import Role

#Class encapsulates a user as an object.
class User(object):
    """
    Attributes:
        firstname
        lastname
        email
        role
    """
    #Returns a new User object.
    def __init__(self, firstname, lastname, email, role):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = Role(role)

    def getFullName(self):
        return self.firstname + " " + self.lastname