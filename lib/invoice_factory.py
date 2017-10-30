#!/usr/bin/env python

"""Generates Invoice"""

from lib import data_posgresql as pg
from time import strftime
from tabulate import tabulate

__author__     = "Jacques Troussard"
__date__       = "Sun Oct 29 2017"

def makeInvoice(invoice_data, invoice_number): # invoice_name - list of dicts where dict is line
    result = True # Return value for validation
    invoice_directory = "invoices/"
    file_name = "{}{}-{}{}".format(invoice_directory, str(int(invoice_number) + 100), strftime("%m"), strftime("%y"))
    # Think about error checking when opening a file
    # From Python Docs: 
    #   Open file and return a corresponding file object. If the file cannot be 
    #   opened, an OSError is raised.
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
    cust_bizn = "Customer Business Name" # is_business boolean - can we add to db
    cust_name = invoice_data[0]['customer']
    cust_addr = "456 Customer Lane" # Issue cust data comes from where? User Input?
    cust_city = "Fredericksburg"
    cust_stat = "VA"
    cust_zipc = 22401
    
    cust_details = [cust_bizn, cust_name, cust_addr, cust_city, cust_stat, cust_zipc]
    
    
    invoice_header = "<BG Distributive Group Company Name> INVOICE"
    todays_date = strftime("%a, %d %b %Y")
    table_header = "product name             part number           qty    price    total amount" # 75 characters long
    
    # Write up to the table
    # VENDOR DETAILS
    for element in vendor_details:
        if element:
            output_file.write("{:>75}\n".format(element))
    
    # CUSTOMER DETAILS
    output_file.write("{:<}".format("TO:\n"))
    for element in cust_details:
        if element:
            output_file.write("{:<}\n".format(element))
    
    # INVOICE DETAILS
    output_file.write("\n\n{:^75}\nInvoice Number: {:<75}\nDate: {:<75}\n\n".format(invoice_header, invoice_number, todays_date))
    
    tabulate.PRESERVE_WHITESPACE = True
    # Write Table
    table = []
    for line in invoice_data:
        # Tabulate line format - need to pad name somehow
        tab_line = []
        name = pg.getProductName(line['product'])[0]
        if len(name) < 40:
            name = "{:<40}".format(name)
        elif len(name) > 42:
            name = "{}...".format(name[:37])
            
        tab_line.append(name)
        tab_line.append(line['product'])
        tab_line.append(str(line['qty']))
        tab_line.append(str(pg.getProductPrice(line['product'])))
        tab_line.append(str(float(pg.getProductPrice(line['product'])) * int(line['qty'])))
        table.append(tab_line)
        output_file.write(tabulate(table, headers=["Description", "Part Number", "Qty", "Price", "Total"], tablefmt="simple", stralign="left", numalign="decimal"))

        # Get product price and total
        price = pg.getProductPrice(line['product'])
        total = float(price) * int(line['qty'])
        
        # Print footer
        table_footer = "{:>{offset}}{}".format("Grand Total $", total, offset=75-len(str(total)))
        output_file.write("\n\n\n")
        output_file.write(table_footer)
            
    return result