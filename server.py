import os
import uuid
import binascii

from lib.config import *
from lib import data_posgresql as pg
from lib import tools as tl
from lib import invoice_factory
from lib.User import User
from lib.Role import Role
from lib.transaction import processFile
from flask import Flask, render_template, request, session
from flask import send_file

app = Flask(__name__)
app.secret_key=binascii.hexlify(os.urandom(24)).decode()
#session variable: username (fullname), email

# Error no encode for bytes keeping incase hexlify has issues on another machine
#app.secret_key=os.urandom(24).encode('hex')

#Root mapping
@app.route('/', methods=['GET', 'POST'])
def mainIndex():
	user = None
	attempted = False
	sessionUser=['','', '']
	#Log in user
	if request.method == 'POST':
		attempted = True
		email=request.form['email']
		pwd=request.form['pwd']
		query = pg.logIn(email, pwd)
		if query != None  and len(query) > 0:
			user = User(query[0], query[1], query[2], query[3])
			session['userName'] = user.firstname
			session['email'] = user.email
			session['role'] = user.role.value
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','']
	return render_template('index.html', sessionUser=sessionUser, attempted=attempted)

@app.route('/logout')
def logout():
	if 'email' in session:
		session.clear()
	if 'userName' in session: 	# Determine if the user is logged in.
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser = ['', '', '']
	attempted=False
	return render_template('index.html', sessionUser=sessionUser, attempted=attempted)
	
#Displays the Import page to import a document
@app.route('/import', methods=['GET', 'POST'])
def importPage():
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','', '']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	if request.method == 'GET':
		return render_template('import.html', post=False, sessionUser=sessionUser)
	tmpfile = 'tmp.csv'
	file = request.files['csvfile']
	file.save(tmpfile)
	result = processFile(tmpfile)
	print(result)
	os.remove(tmpfile)
	return render_template('import.html', post=True, result=result, sessionUser=sessionUser)

#Displays the Invoice page to create and displays invoices	
@app.route('/invoice')
def invoicePage():
	count = 0;
	# 
	if request.method == 'GET':
		count = pg.countInvoices()
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	return render_template('invoice.html', count=count, sessionUser=sessionUser)
	
# Renders create invoice form/page
@app.route('/invCreate', methods=['GET', 'POST'])
def invCreatePage():
	invoiceData = [] # list of dictionaries
	invoiceNumber = -1 # Invoice data input integrity
	inv_alert = ""
	invoice_doc = None
	inv_file_data = []
	
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','', '']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	if request.method == 'GET':
		return render_template('invCreate.html', post=False, sessionUser=sessionUser)

	# Create new invoice (sale)
	if request.method == 'POST':
		# Debugging stuff
		tl.printDict(request.form)
		#print(request.form.getlist('products[]'))
		invoiceData.append({'customer':request.form['customer'], 
		'seller':request.form['seller'], 'date':request.form['date'],
		'products[]':request.form.getlist('products[]'), 'qtys[]':request.form.getlist('qtys[]')})
		invoiceNumber = pg.makeSale(invoiceData)

		if (invoiceNumber > 0):
			# Create invoice doc
			invoice_doc = invoice_factory.makeInvoice(invoiceData, invoiceNumber)
			inv_file_data = invoice_doc
			if invoice_doc:
				inv_alert = "success"
			else:
				inv_alert = "failed" # On creation - see makeInvoice
		else:
			inv_alert = "failed" # On number generation - see makeSale
		
	if request.method == 'GET':
		if (inv_alert == "success"):
			pass
		elif (inv_alert == "failed"):
			pass
		else:
			inv_alert = None

	return render_template('invCreate.html', inv_alert=inv_alert, invoiceNumber=invoiceNumber, invoice_doc=invoice_doc, inv_file_data=inv_file_data, sessionUser=sessionUser)

# Renders search invoice form/page 
@app.route('/invSearch', methods=['GET', 'POST'])
def invDisplayPage():
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)

	results = []
	if request.method == 'POST':
		term = request.form.get('keyword')
		start = request.form.get('start')
		end = request.form.get('end')
		results = pg.invSearch(term, start, end)
	return render_template('invSearch.html', sessionUser=sessionUser, results=results)


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
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	return render_template('products.html', results=results, isSearching=isSearching, searchString=searchString, sessionUser=sessionUser)

#
@app.route('/accounts')
def accountsPage():
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	userList = pg.listAllUsersWithWarehouses()
	return render_template('accounts.html', sessionUser=sessionUser, userList=userList)
	
# Returns generated invoice as attachment
@app.route('/invoices', methods=['GET'])
def invoiceReturnPage():
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('invoice.html', sessionUser=sessionUser, attempted=False)

	number = request.args.get('num', default = 1, type = str)
	extension = request.args.get('ext', default = 1, type = str)
	file = "invoices/" + number + extension
	return send_file(file, as_attachment=True)
	
	
	


# start the server
if __name__ == '__main__':
	#app.run( host='0.0.0.0', port=80, debug=True) #For prod environment
    app.run(host=os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)), debug=True)
	
