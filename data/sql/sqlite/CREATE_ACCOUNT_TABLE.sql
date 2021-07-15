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
	account_route_nbr TEXT(50),
	account_open_amt REAL DEFAULT 0 NOT NULL,
	account_est_amt REAL,
	budget_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	updt_dt_tm REAL NOT NULL,
	updt_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
