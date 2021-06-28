/**
 * Name: CONFIG.sql
 * Purpose: Creates the CONFIG table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE CONFIG (
	config_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	config_text TEXT(100) NOT NULL,
	config_value_int INTEGER,
	config_value_flt REAL,
	config_value_txt TEXT(100),
	config_value_set INTEGER DEFAULT 1 NOT NULL,
	user_id INTEGER NOT NULL,
	create_dt_tm REAL NOT NULL,
	create_iso_ts TEXT(30) NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);
