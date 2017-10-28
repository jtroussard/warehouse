#!/usr/bin/python

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
        self.role = role
