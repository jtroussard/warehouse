# Database access objects stored outside of controller.

import psycopg2
import psycopg2.extras
from lib import tools as tl
from flask import Markup

from lib.config import *

# Connect to the postgreql database.
# Returns a connection object if connection was successful, or None if can't connect.
def connectToPostgres():
  connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST)
  print (connectionString)
  # BP2  Use try-except blocks
  try:
    return psycopg2.connect(connectionString)
  except Exception as e:    # BP2 especially this part where you print the exception
  	print(type(e))
  	print(e)
  	print("Can't connect to database")
  	return None


# generic execute statement
# select=True if it is a select statement
#        False if it is an insert
#
def execute_query(query, conn, select=True, args=None):
	print("in execute query")
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	results = None
	try: 
		quer = cur.mogrify(query, args)   # BP6  never use Python concatenation
		                                  # for database queries
		print(quer)
		cur.execute(quer)
		if select:
			results = cur.fetchall()
		conn.commit()   # BP5  commit and rollback frequently
	except Exception as e:
		conn.rollback()
		print(type(e))
		print(e)
	cur.close()      # BP3 Dispose of old cursors as soon as possible
	return results

#Returns a User if entry matches, or false to reject if no match.
def logIn(email, password):
  conn = connectToPostgres()
  if conn == None:
    return None
  query_string = "SELECT firstname, lastname, email, role from users where email=%s and password=crypt(%s, password);"
  result = execute_query(query_string, conn, args=(email, password))
  conn.close()
  if result != None and len(result) > 0:
  	result = result[0]
  return result

#Search database for products by name, number, and location.
def searchForProducts(productName, productNumber, warehouse):
	conn = connectToPostgres()
	if conn == None:
		return None
	results = None
	query_string = "SELECT p.id, p.pnumber, p.name, p.price, i.warehouseid, w.tag_number, i.quantity from inventory i join products p on i.productid = p.id join warehouses w on i.warehouseid=w.id WHERE "
	if (productName != "" and productNumber != "" and warehouse != ""):  #1 name, number, and warehouse
		query_string += "lower(p.name) like lower(%s) AND lower(p.pnumber)=lower(%s) AND i.warehouseid=%s ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(productName, productNumber, warehouse,))
	elif (productName != "" and productNumber != "" and warehouse == ""): #2 name, number
		query_string += "lower(p.name) like lower(%s) AND lower(p.pnumber)=lower(%s) ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(productName, productNumber,))
	elif (productName == "" and productNumber != "" and warehouse != ""): #3 number, warehouse
		query_string += "lower(p.pnumber)=(%s) AND i.warehouseid=%s ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(productNumber, warehouse,))
	elif (productName != "" and productNumber == "" and warehouse != ""):  #4 name, warehouse
		query_string += "lower(p.name) like lower(%s) AND i.warehouseid=%s ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(productName, warehouse,))
	elif (productName != "" and productNumber == "" and warehouse == ""):  #5 name
		query_string += "lower(p.name) like lower(%s) ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(productName,))
	elif (productName == "" and productNumber != "" and warehouse == ""):  #6 number
		query_string += "lower(p.pnumber)=lower(%s) ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(productNumber,))
	elif (productName == "" and productNumber == "" and warehouse != ""):  #7 warehouse
		query_string += "i.warehouseid=%s ORDER BY p.pnumber, i.warehouseid;"
		results = execute_query(query_string, conn, args=(warehouse,))
	#else if all are blank, return empty results.
	conn.close()
	return results
	
# Return int representing number of rows in table.
def countInvoices():
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT COUNT(DISTINCT saleid) FROM sold";
	results = execute_query(query_string, conn, select=True, args=None)
	conn.close()
	results = results[0][0]
	return results
	
# Return list of sellers - NOT FINISHED
def getSellers():
	conn = connectToPostgres()
	if conn == None:
		return None
	
# Insert sales record into DB (via approperaite tables)
def makeSale(invoiceData):
	conn = connectToPostgres()
	if conn == None:
		return None
	preOp = countInvoices() # Used to confirm invoice hit server
	# Insert sale row - select set as true for returning invoice number
	saleData = [invoiceData[0]['date'], invoiceData[0]['seller'], invoiceData[0]['customer']]
	query_string = "INSERT INTO sales (datesold, seller, customerid) VALUES (%s, %s, %s) RETURNING id;"
	results = execute_query(query_string, conn, select=True, args=(tuple(saleData)))
	if results:
		invoiceNumber = results[0][0]
	else:
		return -1
	
	# Insert sold rows
	line_item_count = len(invoiceData[0]["products[]"])
	for index in range(line_item_count):
		productid = getProductId(invoiceData[0]["products[]"][index], conn)
		quantity = invoiceData[0]["qtys[]"][index]
		
		soldData = [invoiceNumber, productid, quantity]
		query_string = "INSERT INTO sold (saleid, productid, quantity) VALUES (%s, %s, %s);"
		execute_query(query_string, conn, select=False, args=(tuple(soldData)))
	# Clean up return outcome
	conn.close()
	if (preOp < countInvoices()):
		return invoiceNumber
	else:
		return -1
		
# 
def getProductPrice(part_number):
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT price FROM products WHERE pnumber = %s;"
	results = execute_query(query_string, conn, select=True, args=(part_number,))
	if results:
		return results[0][0]
		
# Return product name via part number
# Ideally returns one result in list
# results[0]
def getProductName(part_number):
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT name FROM products WHERE pnumber = %s;"
	results = execute_query(query_string, conn, select=True, args=(part_number,))
	return results[0]
	
def getProductId(part_number, conn=None):
	conn = connectToPostgres()
	if conn == None:
		return None	
	query_string = "SELECT id FROM products WHERE pnumber = %s;"
	results = execute_query(query_string, conn, select=True, args=(part_number,))
	if results:
		productid = results[0][0]
		return productid
	return -1
	
# RETURN a list of rows with keys {id, datesold, assoc, cust, total}
def invSearch(term, start, end):
	term = '%{}%'.format(term)
	start = start if start else '-infinity'
	end = end if end else 'infinity'
	db = connectToPostgres()
	query = '''
	SELECT
		sales.id as id,
		sales.datesold as datesold,
		users.firstname || ' ' || users.lastname as assoc,
		customers.name as cust,
		(SELECT SUM(price * sold.quantity) FROM products JOIN sold ON sold.saleid = sales.id WHERE id = sold.productid) as total
	FROM sales
		JOIN users ON sales.seller = users.email
		JOIN customers ON sales.customerid = customers.id
	WHERE
		(sales.customerid IN (SELECT id FROM customers WHERE name LIKE %s)
		OR users.firstname LIKE %s
		OR users.lastname LIKE %s)
		AND sales.datesold >= %s AND sales.datesold <= %s
	ORDER BY sales.datesold DESC, users.lastname, users.firstname;'''
	invs = execute_query(query, db, True, (term, term, term, start, end))
	db.close()
	return invs

#Selects all user information and warehouse info as needed.
def listAllUsersWithWarehouses():
  conn = connectToPostgres()
  if conn == None:
    return None
  query_string = "SELECT u.firstname, u.lastname, u.email, u.role, u.password, w.id, w.tag_number from users u left outer join warehouses w on u.email = w.associate ORDER BY email;"
  result = execute_query(query_string, conn)
  conn.close()
  return result
  
#Selects all user information and warehouse info as needed, given an email.
def listUserandWarehouseByEmail(email):
  conn = connectToPostgres()
  if conn == None:
    return None
  query_string = "SELECT u.firstname, u.lastname, u.email, u.role, w.id, w.tag_number from users u left outer join warehouses w on u.email = w.associate WHERE email like %s;"
  results = execute_query(query_string, conn, args=(email,))
  conn.close()
  if results:
  	result = results[0]
  return result

#Selects a list of warehosues.
def listAllWarehouses():
  conn = connectToPostgres()
  if conn == None:
    return None
  query_string = "SELECT id, make, model, tag_number from warehouses ORDER BY id;"
  result = execute_query(query_string, conn)
  conn.close()
  return result

#Selects a list of warehosues with users.
def listAllWarehousesWithUsers():
  conn = connectToPostgres()
  if conn == None:
    return None
  query_string = "SELECT id, make, model, tag_number, associate from warehouses ORDER BY id;"
  result = execute_query(query_string, conn)
  conn.close()
  return result
 
#Creates a new system user. 
def createUser(firstname, lastname, email, password, role):
	conn = connectToPostgres()
	if conn == None:
	  return None
	newEmailCheck = "SELECT firstname, lastname, email, role from users where email=%s;"
	emailCheckResult = execute_query(newEmailCheck, conn, args=(email,))
	if not emailCheckResult:
	  insert_user = "INSERT INTO users (firstname, lastname, email, password, role) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);"
	  execute_query(insert_user, conn, select=False, args=(firstname, lastname, email, password, role))
	  emailCheckResult = execute_query(newEmailCheck, conn, args=(email,))
	else:
		emailCheckResult = None
	conn.close()
	return emailCheckResult

#Updates user with new information.
def updateUser(firstname, lastname, email, password, role):
	conn = connectToPostgres()
	if conn == None:
		return None
	result = None
	if password:
		query_string = "UPDATE users SET firstname=%s, lastname=%s, password=crypt(%s, password), role=%s where email=%s;"
		execute_query(query_string, conn, select=False, args=(firstname, lastname, password, role, email,))
	else: 
	#No password udpate.
		query_string = "UPDATE users SET firstname=%s, lastname=%s, role=%s where email=%s;"
		execute_query(query_string, conn, select=False, args=(firstname, lastname, role, email))
	#Check the update was successful
	if password:
		query_string = "SELECT firstname, lastname, email, role from users where firstname=%s and lastname=%s and email=%s and password=crypt(%s, password) and role=%s;"
		result = execute_query(query_string, conn, args=(firstname, lastname, email, password, role,))
	else:
		query_string = "SELECT firstname, lastname, email, role from users where firstname=%s and lastname=%s and email=%s and role=%s;"
		result = execute_query(query_string, conn, args=(firstname, lastname, email, role,))
	conn.close()
	return result


#Updates user association to warehouse by id.
def updateWarehouseAssociate(email, id):
  conn = connectToPostgres()
  if conn == None:
    return None
  query_clear = "UPDATE warehouses SET associate='' where associate=%s;"
  execute_query(query_clear, conn, select=False, args=(email,))
  if id:
  	query_string = "UPDATE warehouses SET associate=%s where id=%s;"
  	execute_query(query_string, conn, select=False, args=(email, id,))
  conn.close()

#Creates a new warehouse.
def createWarehouse(make, model, tagNumber):
	conn = connectToPostgres()
	if conn == None:
	  return None
	insert_user = "INSERT INTO warehouses (make, model, tag_number) VALUES (%s, %s, %s);"
	execute_query(insert_user, conn, select=False, args=(make, model, tagNumber))
	conn.close()


def getCustomers():
	db = connectToPostgres()
	query = 'SELECT * FROM customers ORDER BY name;'
	result = execute_query(query, db, True, ())
	db.close()
	return result

def getCust(ID):
	db = connectToPostgres()
	query = 'SELECT * FROM customers WHERE id = %s;'
	result = execute_query(query, db, True, (ID,))
	db.close()
	return result[0]

def updateCust(data):
	db = connectToPostgres()
	query = '''UPDATE customers SET
		name = %s,
		description = %s,
		address1 = %s,
		address2 = %s,
		city = %s,
		state = %s,
		zipcode = %s,
		phone = %s,
		contact = %s,
		email = %s WHERE id = %s;'''
	args = (data['name'],
		data['description'],
		data['address1'],
		data['address2'],
		data['city'],
		data['state'],
		data['zipcode'],
		data['phone'],
		data['contact'],
		data['email'],
		data['id'])
	execute_query(query, db, False, args)
	db.close()

def createCust(data):
	db = connectToPostgres()
	query = '''INSERT INTO customers
	(name, description, address1, address2, city, state, zipcode, phone, contact, email)
	 VAlUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
	args = (data['name'],
		data['description'],
		data['address1'],
		data['address2'],
		data['city'],
		data['state'],
		int(data['zipcode']),
		data['phone'],
		data['contact'],
		data['email'])
	execute_query(query, db, False, args)
	db.close()
	
def getWarehouse(associate):
	db = connectToPostgres()
	query = 'SELECT w.id from warehouses w inner join users u on w.associate = u.email where u.email = %s';
	result = execute_query(query, db, True, (associate,))
	db.close()
	if len(result) == 1:
		return result[0][0]
	else:
		print("===ERROR===\n  Warehouse id selection error")
		return -1
		
def getWhouseQty(product_id, warehosue_id):
	db = connectToPostgres()
	query = 'SELECT quantity FROM inventory WHERE warehouseid = %s AND productid = %s';
	result = execute_query(query, db, True, (associate,))
	db.close()
	if len(result) == 1:
		return result[0][0]
	else:
		print("===ERROR===\n  Inventory qty retrieval error")
		return -1
		
def reconcile(product_id, warehouse_id, qty_sold):
	print("PASSED INTO QUERY (reconcile) {}".format(product_id))
	db = connectToPostgres()
	query = 'SELECT quantity FROM inventory WHERE warehouseid = %s AND productid = %s';
	result = execute_query(query, db, True, (warehouse_id, product_id))
	if len(result) == 1: # check for return
		if int(qty_sold) < int(result[0][0]):
			balance =  int(result[0][0]) - int(qty_sold)
			query = 'UPDATE inventory SET quantity = %s WHERE warehouseid = %s AND productid = %s';
			args = (balance, warehouse_id, product_id)
			execute_query(query, db, False, args)
			db.close()
			return True
		else:
			db.close()
			return False
	
def checkSaleIntegrity(product_num, warehouse_id, qty_sold):
	product_id = getProductId(product_num)
	db = connectToPostgres()
	query = 'SELECT quantity FROM inventory WHERE warehouseid = %s AND productid = %s';
	result = execute_query(query, db, True, (warehouse_id, product_id))
	db.close()
	# YOU SHALL NOT PASS --- MAYBE
	if len(result) < 1: # check for return
		if product_id < 0: # bad product number
			product_id = "Unknown"
			message = Markup("<br><p><strong>ErrorType:</strong> Query Fault<br><strong>Warehouse:</strong> {}<br><strong>ProductNum:</strong> {}</p><p>Database unchanged.</p>".format(warehouse_id, product_id))
			return message
		if warehouse_id < 0: # bad seller info
			warehouse_id = "Unknown"
			message = Markup("<br><p><strong>ErrorType:</strong> Query Fault<br><strong>Warehouse:</strong> {}<br><strong>ProductNum:</strong> {}</p><p>Database unchanged.</p>".format(warehouse_id, product_id))
			return message
	if int(qty_sold) < 0:
		message = Markup("<br><p><strong>ErrorType:</strong> Negative Qty<br><strong>Warehouse:</strong> {}<br><strong>ProductNum:</strong> {}</p><p>Database unchanged.</p>".format(warehouse_id, product_id))
		return message
	if int(qty_sold) > int(result[0][0]):
		message = Markup("<br><p><strong>ErrorType:</strong> Insufficient Inventory<br><strong>Warehouse:</strong> {}<br><strong>ProductNum:</strong> {}</p><p>Database unchanged.</p>".format(warehouse_id, product_id))
		return message
	# YOU SHALL PASS!!!
	return "good"
	
	