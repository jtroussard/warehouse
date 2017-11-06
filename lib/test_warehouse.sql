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
	address1 TEXT,
	address2 TEXT,
	city TEXT,
	state TEXT,
	zipcode INTEGER,
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

insert into warehouses (associate) values
('main'),('taylor'),('sam'), ('jacques');

insert into customers (name, description, address1, city, state, zipcode, contact, phone, email) VALUES
('autozone', 'large autoparts dealer', '123 street avenue', 'Fredericksburt', 'VA', 22401, 'harvey wayne', '0123456789', 'email@email.email'),
('yates', 'local garage', '456 road blvd', 'Alexandria', 'VA', 22301, 'Bruce Dent', '0123456789', 'email@email.email'),
('jiffy lube', 'nationwide garage', '789 lane way', 'Richmond', 'VA', 22501, 'Darius McJohnson', '0123456789', 'email@email.email');

insert into users (email, password, firstname, lastname, role) VALUES
('tdohmen@mail.umw.edu', crypt('123', gen_salt('bf')), 'Taylor', 'Dohmen', 0),
('smiller@mail.umw.edu', crypt('123', gen_salt('bf')), 'Samantha', 'Miller', 0),
('jtroussard@mail.umw.edu',  crypt('123', gen_salt('bf')), 'Jacques', 'Troussard', 0);

insert into sales (datesold, seller, customerid) VALUES
('2017-01-01', 'tdohmen@mail.umw.edu', 1),
('2017-06-06', 'smiller@mail.umw.edu', 2),
('2017-11-11', 'jtroussard@mail.umw.edu', 3),
('2002-04-22', 'tdohmen@mail.umw.edu', 3);

insert into products (pnumber, name, price) values
('1', 'blinker fluid', 111.11),
('2', 'tire fluid', 222.22),
('3', 'airbag fluid', 333.33),
('4', 'radio fluid', 444.44),
('5', 'headrest fluid', 555.55);

insert into sold (saleid, productid, quantity) VALUES
(1, 1, 10),
(1, 4, 500),
(2, 2, 20),
(2, 3, 100),
(3, 1, 1),
(3, 2, 1),
(3, 3, 1),
(3, 4, 1),
(3, 5, 1),
(4, 3, 987);

/*
1.
get warehouse id associated with sales associate
select w.id from users u left outer join warehouses w on u.email = w.associate returning w.id

2.
get qty of product from inventory associated with warehouse id
select quantity from inventory where productid = ... AND warehouseid = ...;

3.
server side compare units sold with current stock return result
- return alert if negative
	- break
- return warning if 0 (restock)
	- process reconcilation
	- update inventory set quantity = returned result where productid = ...;
*/