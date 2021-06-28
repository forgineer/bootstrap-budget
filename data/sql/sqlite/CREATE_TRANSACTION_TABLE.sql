/**
 * Name: CREATE_TRANSACTION_TABLE.sql
 * Purpose: Creates the TRANSACTION table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE "TRANSACTION" (
	transaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	transaction_desc TEXT(200),
	transaction_norm TEXT(200),
	transaction_amt REAL DEFAULT 0 NOT NULL,
	transaction_dt_tm REAL NOT NULL,
	transaction_iso_ts TEXT(30) NOT NULL,
	transaction_note TEXT(500),
	budget_item_id INTEGER DEFAULT 0 NOT NULL,
	account_id INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
