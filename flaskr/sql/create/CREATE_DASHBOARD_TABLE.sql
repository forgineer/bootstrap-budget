/**
 * Name: CREATE_DASHBOARD_TABLE.sql
 * Purpose: Creates the DASHBOARD table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE DASHBOARD (
	dashboard_id serial NOT NULL PRIMARY KEY,
	dashboard_year integer NOT NULL,
	dashboard_month integer NOT NULL,
	budget_id integer NOT NULL,
	budget_item_id integer NOT NULL,
	budget_item_amt real DEFAULT 0.0 NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
