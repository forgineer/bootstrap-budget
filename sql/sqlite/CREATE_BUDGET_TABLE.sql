/**
 * Name: CREATE_BUDGET_TABLE.sql
 * Purpose: Creates the BUDGET table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE BUDGET (
	budget_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	budget_name TEXT(100) NOT NULL,
	budget_desc TEXT(200),
	budget_year INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	updt_dt_tm REAL NOT NULL,
	updt_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
