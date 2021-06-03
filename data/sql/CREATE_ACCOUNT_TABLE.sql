/**
 * Name: CREATE_ACCOUNT_TABLE.sql
 * Purpose: Creates the ACCOUNT table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE ACCOUNT (
	account_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	account_name TEXT(100) NOT NULL,
	account_desc TEXT(500),
	account_nbr TEXT(50),
	route_nbr TEXT(50),
	user_id INTEGER NOT NULL,
	permissions NUMERIC NOT NULL,
	create_dttm TEXT(30) NOT NULL,
	active_ind NUMERIC DEFAULT 1 NOT NULL
);
