import psycopg2
from exceptions import *
from db import *

def processFile(csvName):
	csv = open(csvName, 'r').readlines()
	data = [i.strip().split(',') for i in csv if i[0] != '#']
	db = connect()
	cursor = db.cursor()

	# This may raise exceptions, if so they should be caught up a level or two
	# and used as an indication of invalid formatting
	for i in data:
		if len(i) == 4:
			fromId = int(i[0].strip())
			toId = int(i[1].strip())
			product = i[2].strip()
			transferQuant  = int(i[3].strip())

			qstr = 'SELECT quantity FROM inventory WHERE product = %s AND warehouseid = %s'
			query = cursor.mogrify(qstr, (product, fromId))
			cursor.execute(query)
			fromQuant = cursor.fetchone()[0]

			if fromQuant == None or transferQuant > fromQuant:
				raise Exception('Inventory Overdraft')

			query = cursor.mogrify(qstr, (product, toId))
			cursor.execute(query)
			toQuant = cursor.fetchone()

			qstr = 'UPDATE inventory SET quantity = %s WHERE product = %s AND warehouseid = %s;'
			query = cursor.mogrify(qstr, (fromQuant - transferQuant, product, fromId))
			cursor.execute(query)

			if toQuant:
				query = cursor.mogrify(qstr, (product, toId, toQuant[0] + transferQuant))
			else:
				query = cursor.mogrify(
					'INSERT INTO inventory (product, warehouseid, quantity) VALUES (%s, %s, %s);',
					(product, toId, transferQuant)
				)
			cursor.execute(query)
			db.commit()
		elif len(i) == 5:
			toId = int(i[0].strip())
			prodName = i[1].strip()
			prodDesc = i[2].strip()
			quantity = int(i[3].strip())
			price = float(i[4].strip())
			try:
				query = cursor.mogrify(
					'''INSERT INTO products (name, description, price) VALUES (%s, %s, %s);
					INSERT INTO inventory (product, warehouseid, quantity) VALUES (%s, %s, %s);''',
					(prodName, prodDesc, price, prodName, toId, quantity)
				)
				cursor.execute(query)
			except Exception as e:
				print(e)
		db.commit()
			

