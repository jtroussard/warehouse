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
	
	# Clean up
	conn.close()
	print(results)

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
  print(result)
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
 
def createUser(firstname, lastname, email, password, role):
	conn = connectToPostgres()
	if conn == None:
	  return None
	newEmailCheck = "SELECT firstname, lastname, email, role from users where email=%s;"
	emailCheckResult = execute_query(newEmailCheck, conn, args=(email,))
	print("emailCheckResult")
	if not emailCheckResult:
	  insert_user = "INSERT INTO users (firstname, lastname, email, password, role) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);"
	  execute_query(insert_user, conn, select=False, args=(firstname, lastname, email, password, role))
	  emailCheckResult = execute_query(newEmailCheck, conn, args=(email,))
	else:
		emailCheckResult = None
	conn.close()
	print(emailCheckResult)
	return emailCheckResult

#Updates user with new information.
def updateUser(firstname, lastname, email, password, role):
	conn = connectToPostgres()
	if conn == None:
		return None
	result = None
	if password:
		print("Test if")
		query_string = "UPDATE users SET firstname=%s, lastname=%s, password=crypt(%s, password), role=%s where email=%s;"
		execute_query(query_string, conn, select=False, args=(firstname, lastname, password, role, email,))
	else: 
	#No password udpate.
		print("Test else")
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