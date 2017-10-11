import os
from flask import Flask, render_template
app = Flask(__name__)

#Root mapping
@app.route('/')
def mainIndex():
	return render_template('index.html')
	
#Displays the Import page to import a document
@app.route('/import')
def importPage():
	return render_template('import.html')

#Displays the Invoice page to create and displays invoices	
@app.route('/invoice')
def invoicePage():
	return render_template('invoice.html')

#Displays a Products page to search for the products the company offers.
@app.route('/products')
def productsPage():
	return render_template('products.html')


# start the server
if __name__ == '__main__':
	#app.run( host='0.0.0.0', port=80, debug=True) #For prod environment
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)