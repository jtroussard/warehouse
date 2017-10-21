#!/usr/bin/env python

"""Custom Debug Tools"""

__author__     = "Jacques Troussard"
__date__       = "10/21/2017"
__version__    = "0.0.0"

# Insert sales record into DB (via approperaite tables)
def printDict(d):
	# Type check
	print(type(d))
	
	# Print
	for k,v in d.items():
		print ("k: {}, d: {}".format(k,v))