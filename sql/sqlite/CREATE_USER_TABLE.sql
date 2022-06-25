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
	username TEXT(40) NOT NULL,
	address_line_1 TEXT(100),
	address_line_2 TEXT(100),
	city TEXT(100),
	state TEXT(50),
	zipcode TEXT(20),
	email TEXT(100),
	phone_number TEXT(10),
	hash TEXT(100),
	salt TEXT(100),
	tutorial_ind INTEGER DEFAULT 1,
	admin_ind INTEGER DEFAULT 0 NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	updt_dt_tm REAL NOT NULL,
	updt_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
