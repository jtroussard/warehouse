DROP DATABASE IF EXISTS warehouse2;
CREATE DATABASE warehouse2;
\c warehouse2;

DROP TABLE IF EXISTS warehouses CASCADE;
DROP SEQUENCE IF EXISTS warehouses_id_seq;
DROP TABLE IF EXISTS products CASCADE;
DROP SEQUENCE IF EXISTS products_id_seq;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP SEQUENCE IF EXISTS customers_id_seq;
DROP TABLE IF EXISTS sales CASCADE;
DROP SEQUENCE IF EXISTS sales_id_seq;
DROP TABLE IF EXISTS sold CASCADE;

CREATE EXTENSION pgcrypto;

CREATE TABLE warehouses (
	id serial NOT NULL PRIMARY KEY,
	associate TEXT,
	tag_number TEXT, 
	make TEXT,
	model TEXT
	-- any other fields for this?
);

CREATE TABLE products (
	id serial NOT NULL PRIMARY KEY,
	pnumber TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL,
	description TEXT,
	price DECIMAL NOT NULL
);

CREATE TABLE inventory (
	productid INTEGER NOT NULL,
	warehouseid INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	PRIMARY KEY (productid, warehouseid),
	FOREIGN KEY (productid) REFERENCES products(id),
	FOREIGN KEY (warehouseid) REFERENCES warehouses(id)
);

CREATE TABLE users (
	email TEXT NOT NULL PRIMARY KEY,
	password TEXT NOT NULL,
	firstname TEXT NOT NULL,
	lastname TEXT NOT NULL,
	role INTEGER NOT NULL
);

CREATE TABLE customers (
	id serial NOT NULL PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT,
	address TEXT,
	phone TEXT,
	contact TEXT,
	email text
);

CREATE TABLE sales (
	id serial NOT NULL PRIMARY KEY,
	datesold DATE NOT NULL,
	seller TEXT NOT NULL,
	customerid INTEGER NOT NULL,
	FOREIGN KEY (seller) REFERENCES users(email),
	FOREIGN KEY (customerid) references customers(id)
);

CREATE TABLE sold (
	saleid INTEGER NOT NULL,
	productid INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	PRIMARY KEY (saleid, productid),
	FOREIGN KEY (saleid) REFERENCES sales(id),
	FOREIGN KEY (productid) REFERENCES products(id)
);

DROP ROLE IF EXISTS whmanager;
CREATE USER whmanager WITH PASSWORD 'iurnf882jdkjop2';
GRANT INSERT, SELECT, UPDATE ON 
	warehouses,
	products,
	inventory,
	users,
	customers,
	sales,
	sold
TO whmanager;
GRANT SELECT, UPDATE ON
	warehouses_id_seq,
	products_id_seq,
	customers_id_seq,
	sales_id_seq
TO whmanager;

/* Adding dummy sales person for db testing */
INSERT INTO users VALUES (
	't.stark@stark-international.com', 
	'password', 
	'Tony', 
	'Stark', 
	0
);

INSERT INTO users VALUES (
	'jacques.troussard@gmail.com',
	crypt('jackdale', gen_salt('bf')),
	'Jacques',
	'Troussard',
	0
);

INSERT INTO customers VALUES (
	0,
	'George Washington'
);

INSERT INTO products VALUES (
	0,
	'sm-65484',
	'Strange Liquid: Mechanic-in-a-Can',
	'Fix anything. Pour in washer fluid reservoir. 8oz bottle',
	9.99
);

INSERT INTO products VALUES (
	1,
	'sm-12345',
	'Blue Stuff',
	'Clean anything.',
	0.59
);

