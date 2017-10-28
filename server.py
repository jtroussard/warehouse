import os
import uuid
import binascii

from lib.config import *
from lib import data_posgresql as pg
from lib import tools as tl
from lib.User import User
from lib.Role import Role
from lib.transaction import processFile
from flask import Flask, render_template, request, session

app = Flask(__name__)
<<<<<<< HEAD
#app.secret_key=os.urandom(24).encode('hex') 
app.secret_key=binascii.hexlify(os.urandom(32)).decode()
#session variable: username (fullname), email, role
=======
app.secret_key=binascii.hexlify(os.urandom(24)).decode()
#app.secret_key=os.urandom(24).encode('hex') # gives attr error no encode for bytes keeping incase hexlify has issues on another machine
#session variable: username (fullname), email
>>>>>>> master

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
	# Create new invoice (sale)
	if request.method == 'POST':
		# Debugging stuff
		tl.printDict(request.form)
		
		# Multiple items not supported at this point
		invoiceData.append({'customer':request.form['customer'], 
		'seller':request.form['seller'], 'date':request.form['date'], 
		'product':request.form['product'], 'qty':request.form['qty']})
		pg.makeSale(invoiceData)
		#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	return render_template('invCreate.html', sessionUser=sessionUser)
	
# Renders search invoice form/page 
@app.route('/invDisplay')
def invDisplayPage():
	#Session Check
	if 'userName' in session:
		sessionUser = [session['userName'], session['email'], session['role']]
	else:
		sessionUser=['','','']
		return render_template('index.html', sessionUser=sessionUser, attempted=False)
	return render_template('invSearch.html', sessionUser=sessionUser)

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

# Renders search invoice form/page 
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
	
	


# start the server
if __name__ == '__main__':
	#app.run( host='0.0.0.0', port=80, debug=True) #For prod environment
    app.run(host=os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)), debug=True)
	
