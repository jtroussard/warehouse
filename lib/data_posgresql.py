# Samantha Miller (smiller3)
# CPSC-350:  Applications of Databases
# Database access objects stored outside of controller.

import psycopg2
import psycopg2.extras

from lib.config import *

# Connect to the postgreql database.
# Returns a connection object if connection was successful, or None if can't connect.
def connectToPostgres():
  connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST)
  print connectionString
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
	print "in execute query"
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
	print(results)
	return results

#Search database for products by name, number, and location.
def searchForProducts(productName, productNumber, warehouse):
	conn = connectToPostgres()
	if conn == None:
		return None
	results = None
	query_string = "SELECT p.id, p.pnumber, p.name, p.price, i.warehouseid, w.tag_number, i.quantity from inventory i join products p on i.productid = p.id join warehouses w on i.warehouseid=w.id WHERE "
	if (productName != "" and productNumber != "" and warehouse != ""):  #1 name, number, and warehouse
		query_string += "lower(p.name) like lower(%s) AND lower(p.pnumber)=lower(%s) AND i.warehouseid=%s;"
		results = execute_query(query_string, conn, args=(productName, productNumber, warehouse,))
	elif (productName != "" and productNumber != "" and warehouse == ""): #2 name, number
		query_string += "lower(p.name) like lower(%s) AND lower(p.pnumber)=lower(%s);"
		results = execute_query(query_string, conn, args=(productName, productNumber,))
	elif (productName == "" and productNumber != "" and warehouse != ""): #3 number, warehouse
		query_string += "lower(p.pnumber)=(%s) AND i.warehouseid=%s;"
		results = execute_query(query_string, conn, args=(productNumber, warehouse,))
	elif (productName != "" and productNumber == "" and warehouse != ""):  #4 name, warehouse
		query_string += "lower(p.name) like lower(%s) AND i.warehouseid=%s;"
		results = execute_query(query_string, conn, args=(productName, warehouse,))
	elif (productName != "" and productNumber == "" and warehouse == ""):  #5 name
		query_string += "lower(p.name) like lower(%s);"
		results = execute_query(query_string, conn, args=(productName,))
	elif (productName == "" and productNumber != "" and warehouse == ""):  #6 number
		query_string += "lower(p.pnumber)=lower(%s);"
		results = execute_query(query_string, conn, args=(productNumber,))
	elif (productName == "" and productNumber == "" and warehouse != ""):  #7 warehouse
		query_string += "i.warehouseid=%s;"
		results = execute_query(query_string, conn, args=(warehouse,))
	#else if all are blank, return empty results.
	conn.close()
	return results

# Creates a new user for TMS
# def registerUser(firstName, lastName, password, email, club, region, wantsNews):
#   conn = connectToPostgres()
#   if conn == None:
#     return None
#   #crypt(%s, gen_salt('bf')) - use in later lecture?
#   query_string = "INSERT INTO users (first_name, last_name, password, email, club, region, wants_news) VALUES (%s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s);"
#   execute_query(query_string, conn, select=False,  args=(firstName, lastName, password, email, club, region, wantsNews))
#   conn.close()
  
# # Returns a list of all users on the site
# def listAllUsers():
#   conn = connectToPostgres()
#   if conn == None:
#     return None
#   query_string = "SELECT first_name, last_name, club, region from users;"
#   results = execute_query(query_string, conn)
#   conn.close()
#   return results

# # Returns a list of all users on the site, given an identifying email.
# def listRegionUsers(email):
#   conn = connectToPostgres()
#   if conn == None:
#     return None
#   print(email)
#   results = None
#   query_string1 = "SELECT region from users WHERE email=%s;"
#   selectedRegion = execute_query(query_string1, conn, args=(email,))
#   if selectedRegion != None:
#     print(selectedRegion)
#     print(selectedRegion[0][0])
#     query_string2 = "SELECT first_name, last_name, club, region from users where region=%s;"
#     results = execute_query(query_string2, conn, args=(selectedRegion[0][0],))
#   conn.close()
#   return results

# # Returns true if user is logged into site
# def logIn(email, password):
#   conn = connectToPostgres()
#   if conn == None:
#     return None
#   query_string = "SELECT first_name, email from users where email=%s and password=crypt(%s, password);"
#   results = execute_query(query_string, conn, args=(email, password))
#   conn.close()
#   return results
  
