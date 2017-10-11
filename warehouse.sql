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

CREATE TABLE warehouses (
	id serial NOT NULL PRIMARY KEY,
	associate TEXT NOT NULL
	-- any other fields for this?
);

CREATE TABLE products (
	name TEXT NOT NULL PRIMARY KEY,
	description TEXT,
	price DECIMAL NOT NULL
);

CREATE TABLE inventory (
	product TEXT NOT NULL,
	warehouseid INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	PRIMARY KEY (product, warehouseid),
	FOREIGN KEY (product) REFERENCES products(name),
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
	product TEXT NOT NULL,
	quantity INTEGER NOT NULL,
	PRIMARY KEY (saleid, product),
	FOREIGN KEY (saleid) REFERENCES sales(id),
	FOREIGN KEY (product) REFERENCES products(name)
);

DROP ROLE IF EXISTS whmanager;
CREATE USER whmanager WITH PASSWORD 'iurnf882jdkjop2';
GRANT INSERT, SELECT, UPDATE ON warehouses, products, inventory, users, customers, sales, sold TO whmanager;


INSERT INTO warehouses (associate) VALUES
	('manager'),
	('taylor'),
	('samantha'),
	('jacques')
;

-- INSERT INTO products (name, description, price) VALUES
-- 	('oil', 'oil for the engine', 5.99),
-- 	('wipers', 'a pair of windsheild wipers', 105.99),
-- 	('headlight fluid', 'this is how headlights work promise', 54.99),
-- 	('timing belt', 'it does something when it is in your car', 0.99),
-- 	('radio', 'for da tunes', 5555.99)
-- ;