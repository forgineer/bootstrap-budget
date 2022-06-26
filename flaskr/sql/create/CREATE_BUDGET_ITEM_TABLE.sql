/**
 * Name: CREATE_BUDGET_ITEM_TABLE.sql
 * Purpose: Creates the BUDGET_ITEM table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE BUDGET_ITEM (
	budget_item_id serial NOT NULL PRIMARY KEY,
	budget_id integer NOT NULL,
	budget_item_name varchar(100) NOT NULL,
	budget_item_desc varchar(200),
	budget_item_amt real DEFAULT 0.0 NOT NULL,
	budget_item_seq integer DEFAULT 99 NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
