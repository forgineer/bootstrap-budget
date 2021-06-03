/**
 * Name: CREATE_USER_TABLE.sql
 * Purpose: Creates the USER table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE "USER" (
	user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	last_name TEXT(100) NOT NULL,
	first_name TEXT(100) NOT NULL,
	middle_name TEXT(100),
	login TEXT(20) NOT NULL,
	address_line_1 INTEGER,
	address_line_2 TEXT(100),
	city TEXT(100),
	state TEXT(50),
	zipcode TEXT(20),
	email TEXT(100),
	phone_number TEXT(10),
	admin_ind NUMERIC DEFAULT 0 NOT NULL,
	hash TEXT(50) NOT NULL,
	salt TEXT(50) NOT NULL,
	create_dttm TEXT(30) NOT NULL,
	active_ind NUMERIC DEFAULT 1 NOT NULL
);
