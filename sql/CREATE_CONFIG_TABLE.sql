/**
 * Name: CONFIG.sql
 * Purpose: Creates the CONFIG table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE CONFIG (
	config_id serial NOT NULL PRIMARY KEY,
	config_varchar varchar(100) NOT NULL,
	config_value_int integer,
	config_value_flt real,
	config_value_txt varchar(100),
	config_value_set integer DEFAULT 0 NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm real NOT NULL,
	create_iso_ts varchar(30) NOT NULL,
	updt_dt_tm real NOT NULL,
	updt_iso_ts varchar(30) NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
