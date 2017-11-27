#!/usr/bin/env python

"""Generates Invoice"""

from lib import data_posgresql as pg
from time import strftime
from tabulate import tabulate

__author__     = "Jacques Troussard"
__date__       = "Sun Oct 29 2017"

def makeInvoice(invoice_data, invoice_number, date): # invoice_name - list of dicts where dict is line
    print("INVOICE DATA --- {}".format(invoice_data))
    result = None # Return value for validation PRINTED INVOICE NUMBER (FILENAME)
    invoice_directory = "invoices/"
    file_name = "{}".format(str(invoice_number))
    file_ext = ".txt"
    full_path = invoice_directory + file_name + file_ext
    # Think about error checking when opening a file
    # From Python Docs: 
    #   Open file and return a corresponding file object. If the file cannot be 
    #   opened, an OSError is raised.
    output_file = open(full_path, "a")
    
    # Invoice formatting based on 8.5" x 11" paper with 0.5" margins (u,l,r,d)
    # - Paper width in monospaced size 12 font = 75
    
    # This can be moved in a configuration file later on
    vendor_name = "BGCVA"
    vendor_adr1 = "123 Main Street"
    vendor_adr2 = ""
    vendor_city = "Ashland"
    vendor_stat = "VA"
    vendor_vipc = 23005
    vendor_phon = 560555555
    vendor_csz = vendor_city + ", " + vendor_stat + " " + str(vendor_vipc)
    # DO NOT CHANGE ORDER
    vendor_details = [vendor_name, vendor_adr1, vendor_adr2, vendor_csz, vendor_phon]
    
    customer = pg.getCust(invoice_data[0]['customer'])
    cust_name = customer['name'] # is_business boolean - can we add to db
    cust_adr1 = customer['address1']
    cust_adr2 = customer['address2']
    if cust_adr2:
        if len(cust_adr2) > 1:
            cust_addr = cust_adr1 + "\n" + cust_adr2
    else:
        cust_addr = cust_adr1
    cust_city = customer['city']
    cust_stat = customer['state']
    cust_zipc = customer['zipcode']
    if customer['phone'] and len(str(customer['phone'])) == 10:
        cust_phne = "({}){}-{}".format(str(customer['phone'][0:3]),str(customer['phone'][3:6]),str(customer['phone'][6:10]))
    elif customer['phone'] and len(str(customer['phone'])) == 11:
        cust_phne = "1({}){}-{}".format(str(customer['phone'][1:4]),str(customer['phone'][4:7]),str(customer['phone'][7:11]))
    else:
        cust_phne = customer['phone']
    cust_csz = cust_city + ", " + cust_stat + " " + str(cust_zipc)
    cust_details = [cust_name, cust_addr, cust_csz, cust_phne]
    
    invoice_header = "INVOICE"
    todays_date = date
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
    line_item_count = len(invoice_data[0]["products[]"])
    grand_total = 0
    for index in range(line_item_count):
        tab_line = []
        part_number = invoice_data[0]["products[]"][index]
        qty_sold = invoice_data[0]["qtys[]"][index]
        name = pg.getProductName(part_number)[0]
        if len(name) < 40:
            name = "{:<40}".format(name)
        elif len(name) > 42:
            name = "{}...".format(name[:37])
        tab_line.append(name)
        tab_line.append(part_number) # Part Number
        tab_line.append(str(qty_sold)) # Qty Sold
        tab_line.append(str(pg.getProductPrice(part_number))) # Unit Price
        line_total = float(pg.getProductPrice(part_number)) * int(qty_sold)
        tab_line.append(str(line_total))
        table.append(tab_line)
        grand_total += line_total
    output_file.write(tabulate(table, headers=["Product Name", "Part Number", "Qty", "Price", "Total"], tablefmt="simple", stralign="left", numalign="decimal"))

    # Print footer
    table_footer = "{:>{offset}}{}".format("Grand Total $", grand_total, offset=75-len(str(grand_total)))
    output_file.write("\n\n\n")
    output_file.write(table_footer)
        
    return [full_path, file_name, file_ext]