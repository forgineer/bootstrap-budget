/**
 * Name: CREATE_TRANSACTION_TABLE.sql
 * Purpose: Creates the TRANSACTION table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE "TRANSACTION" (
	transaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	transaction_desc TEXT(100),
	transaction_amount REAL DEFAULT 0.0 NOT NULL,
	transaction_dttm TEXT(30) NOT NULL,
	account_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	create_dttm TEXT(30) NOT NULL,
	active_ind NUMERIC DEFAULT 1 NOT NULL
);
