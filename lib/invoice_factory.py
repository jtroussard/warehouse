#!/usr/bin/env python

"""Generates Invoice"""

from lib import data_posgresql as pg
from time import strftime

__author__     = "Jacques Troussard"
__date__       = "Sun Oct 29 2017"

def makeInvoice(invoice_data, invoice_number): # invoice_name - list of dicts where dict is line
    result = False
    invoice_directory = "invoices/"
    file_name = "{}{}-{}{}".format(invoice_directory, str(int(invoice_number) * 100), strftime("%m"), strftime("%y"))
    output_file = open(file_name, "a")
    
    # Invoice formatting based on 8.5" x 11" paper with 0.5" margins (u,l,r,d)
    # - Paper width in monospaced size 12 font = 75
    
    # This can be moved in a configuration file later on
    vendor_name = "Business Name"
    vendor_adr1 = "123 Main Street"
    vendor_adr2 = ""
    vendor_city = "Ashland"
    vendor_stat = "VA"
    vendor_vipc = 23005
    vendor_phon = 560555555
    
    # DO NOT CHANGE ORDER
    vendor_details = [vendor_name, vendor_adr1, vendor_adr2, vendor_city, vendor_stat, vendor_vipc, vendor_phon]
    
    # Additional customer details need to banked in db
    cust_bizn = "Customer Business name" # is_business boolean - can we add to db
    cust_name = invoice_data[0]['customer']
    cust_addr = "456 Customer Lane" # Issue cust data comes from where? User Input?
    cust_city = "Fredericksburg"
    cust_stat = "VA"
    cust_zipc = 22401
    
    test_total = 904.31
    total_offset = len(str(test_total))
    invoice_header = "<BG Distributive Group Company Name> Invoice"
    todays_date = strftime("%a, %d %b %Y")
    table_header = "product name             part number           qty    price    total amount" # 75 characters long
    table_footer = "{:>{offset} ${:>75}".format("Grand Total: ", test_total, offset=75-total_offset)
    
    # Write up to the table
    for element in vendor_details:
        if element:
            output_file.write("{:>75}".format(element))
    return result