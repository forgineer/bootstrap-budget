/**
 * Name: CREATE_USER_BUDGET_TABLE.sql
 * Purpose: Creates the USER_BUDGET table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE USER_BUDGET (
	user_budget_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	permissions INTEGER NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	updt_dt_tm REAL NOT NULL,
	updt_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
