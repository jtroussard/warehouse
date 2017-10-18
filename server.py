import os
import uuid

from lib.config import *
from lib import data_posgresql as pg
from lib.transaction import processFile
from flask import Flask, render_template, request, session

app = Flask(__name__)
#app.secret_key=os.urandom(24).encode('hex') #session variable

#Root mapping
@app.route('/')
def mainIndex():
	return render_template('index.html')
	
#Displays the Import page to import a document
@app.route('/import', methods=['GET', 'POST'])
def importPage():
	if request.method == 'GET':
		return render_template('import.html', post=False)
	tmpfile = 'tmp.csv'
	file = request.files['csvfile']
	file.save(tmpfile)
	result = processFile(tmpfile)
	print(result)
	os.remove(tmpfile)
	return render_template('import.html', post=True, result=result)

#Displays the Invoice page to create and displays invoices	
@app.route('/invoice')
def invoicePage():
	return render_template('invoice.html')

#Displays a Products page to search for the products the company offers.
@app.route('/products', methods=['GET', 'POST'])
def productsPage():
	results = []
	searchString = ""
	isSearching = False
	#if post, get info
	if request.method == 'POST':
		isSearching = True
		pnumber = ""
		pname = ""
		warehouse = ""
		if request.form.get("productNumber") != None:
			pnumber=request.form['productNumber']
		if request.form.get("productName") != None:
			pname=request.form['productName']
		if request.form.get("warehouse") != None:
			warehouse=request.form['warehouse']
		#Concatinate search details
		if pnumber != "":
			searchString += "Product number: " + pnumber + " "
		if pname != "":
			searchString += "Product name: " + pname + " "
		if warehouse != "":
			searchString += "Warehouse: " + warehouse
		if pname + pnumber + warehouse == "":
			searchString = "empty string"
		results = pg.searchForProducts(pname, pnumber, warehouse)
	return render_template('products.html', results=results, isSearching=isSearching, searchString=searchString)


# start the server
if __name__ == '__main__':
	#app.run( host='0.0.0.0', port=80, debug=True) #For prod environment
    app.run(host=os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)), debug=True)
	