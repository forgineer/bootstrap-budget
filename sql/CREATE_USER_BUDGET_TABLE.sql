/**
 * Name: CREATE_USER_BUDGET_TABLE.sql
 * Purpose: Creates the USER_BUDGET table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE USER_BUDGET (
	user_budget_id serial NOT NULL PRIMARY KEY,
	user_id integer NOT NULL,
	budget_id integer NOT NULL,
	permissions integer NOT NULL,
	create_dt_tm real NOT NULL,
	create_iso_ts varchar(30) NOT NULL,
	updt_dt_tm real NOT NULL,
	updt_iso_ts varchar(30) NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
