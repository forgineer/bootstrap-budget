/**
 * Name: CREATE_BUDGET_TABLE.sql
 * Purpose: Creates the BUDGET table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE BUDGET (
	budget_id serial NOT NULL PRIMARY KEY,
	budget_name varchar(100) NOT NULL,
	budget_desc varchar(200),
	budget_year integer NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm real NOT NULL,
	create_iso_ts varchar(30) NOT NULL,
	updt_dt_tm real NOT NULL,
	updt_iso_ts varchar(30) NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
