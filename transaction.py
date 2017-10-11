import psycopg2
from exceptions import *
from db import *

INVENTORYUPDATE = 'UPDATE inventory SET quantity = %s WHERE product = %s AND warehouseid = %s;'
INVENTORYINSERT = 'INSERT INTO inventory (product, warehouseid, quantity) VALUES (%s, %s, %s);'
QUANTITY = 'SELECT quantity FROM inventory WHERE product = %s AND warehouseid = %s;'
PRODUCTINSERT = 'INSERT INTO products (name, description, price) VALUES (%s, %s, %s);'

def newProduct(cursor, data):
	toId = int(data[0].strip())
	prodName = data[1].strip()
	prodDesc = data[2].strip()
	quantity = int(data[3].strip())
	price = float(data[4].strip())
	try:
		query = cursor.mogrify(
			PRODUCTINSERT + INVENTORYINSERT, (prodName, prodDesc, price, prodName, toId, quantity)
		)
		cursor.execute(query)
	except Exception as e:
		print(e)

def restock(cursor, data):
	toId = int(data[0].strip())
	product = data[1].strip()
	quantity = int(data[2].strip())
	query = cursor.mogrify(INVENTORYUPDATE, (product, toId, quantity))
	try:
		cursor.execute(query)
	except Exception as e:
		print(e)

def transfer(cursor, data):
	fromId = int(data[0].strip())
	toId = int(data[1].strip())
	product = data[2].strip()
	transferQuant  = int(data[3].strip())

	query = cursor.mogrify(QUANTITY, (product, fromId))
	cursor.execute(query)
	fromQuant = cursor.fetchone()[0]

	if transferQuant > fromQuant:
		raise Exception('Inventory Overdraft')

	query = cursor.mogrify(QUANTITY, (product, toId))
	cursor.execute(query)
	toQuant = cursor.fetchone()

	query = cursor.mogrify(INVENTORYUPDATE, (fromQuant - transferQuant, product, fromId))
	cursor.execute(query)

	if toQuant:
		query = cursor.mogrify(INVENTORYUPDATE, (product, toId, toQuant[0] + transferQuant))
	else:
		query = cursor.mogrify(INVENTORYINSERT, (product, toId, transferQuant))
	cursor.execute(query)

def processFile(csvName):
	csv = open(csvName, 'r').readlines()
	data = [i.strip().split(',') for i in csv if i[0] != '#']
	db = connect()
	cursor = db.cursor()

	# This may raise exceptions, if so they should be caught up a level or two
	# and used as an indication of invalid formatting
	for i in data:
		if len(i) == 3:
			restock(cursor, i)
		elif len(i) == 4:
			transfer(cursor, i)
		elif len(i) == 5:
			newProduct(cursor, i)
	db.commit()
