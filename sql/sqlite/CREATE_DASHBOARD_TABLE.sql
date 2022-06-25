/**
 * Name: CREATE_DASHBOARD_TABLE.sql
 * Purpose: Creates the DASHBOARD table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE DASHBOARD (
	dashboard_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	dashboard_year INTEGER NOT NULL,
	dashboard_month INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	budget_item_id INTEGER NOT NULL,
	budget_item_amt REAL DEFAULT 0 NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	updt_dt_tm REAL NOT NULL,
	updt_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
