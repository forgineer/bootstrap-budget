/**
 * Name: CREATE_BUDGET_ITEM_TABLE.sql
 * Purpose: Creates the BUDGET_ITEM table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE BUDGET_ITEM (
	budget_item_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	budget_item TEXT(100) NOT NULL,
	budget_item_desc TEXT(200),
	budget_item_amt REAL DEFAULT 0 NOT NULL,
	budget_item_prty INTEGER DEFAULT 99 NOT NULL,
	user_id INTEGER NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
