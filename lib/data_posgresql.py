# Database access objects stored outside of controller.

import psycopg2
import psycopg2.extras
from lib import tools as tl

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
	
	preOp = countInvoices()
		
	# Format/Type check data
	# TODO
	
	# Get product id
	# This is part of function testing and should not remain in final code
	# This should be handled via format checking later on
	productName = invoiceData[0]['product']
	query_string = "SELECT id FROM products WHERE pnumber = %s;"
	results = execute_query(query_string, conn, select=True, args=(productName,))
	if results:
		productid = results[0][0]

	# Insert sale row - select set as true for returning id
	saleData = [invoiceData[0]['date'], invoiceData[0]['seller'], invoiceData[0]['customer']]
	query_string = "INSERT INTO sales (datesold, seller, customerid) VALUES (%s, %s, %s) RETURNING id;"
	results = execute_query(query_string, conn, select=True, args=(tuple(saleData)))
	invoiceNumber = results[0][0]
	
	# Insert sold row
	soldData = [invoiceNumber, productid, invoiceData[0]['qty']]
	query_string = "INSERT INTO sold (saleid, productid, quantity) VALUES (%s, %s, %s);"
	results = execute_query(query_string, conn, select=False, args=(tuple(soldData)))
	
	# Clean up return outcome
	conn.close()
	
	if (preOp < countInvoices()):
		return invoiceNumber
	else:
		return -1
	print(results)

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
  query_string = "SELECT u.firstname, u.lastname, u.email, u.role, u.password, w.id, w.tag_number from users u left outer join warehouses w on u.email = w.associate;"
  result = execute_query(query_string, conn)
  conn.close()
  print(result)
  return result
