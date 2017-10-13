import psycopg2

# connects to the database
# edit here if you want to change db user info
def connect():
	dbname = 'warehouse2'
	user = 'whmanager'
	password = 'iurnf882jdkjop2'
	host = 'localhost'
	connectionString = 'dbname={0} user={1} password={2} host={3}'.format(dbname, user, password, host)
	try:
		return psycopg2.connect(connectionString)
	except:
		print("Can't connect to database")
