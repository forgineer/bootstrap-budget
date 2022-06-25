/**
 * Name: CREATE_TRANSACTION_TABLE.sql
 * Purpose: Creates the TRANSACTION table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE TRANSACTION (
	transaction_id serial NOT NULL PRIMARY KEY,
	transaction_desc varchar(200),
	transaction_norm varchar(200),
	transaction_amt real DEFAULT 0 NOT NULL,
	transaction_year integer NOT NULL,
	transaction_month integer NOT NULL,
	transaction_dt_tm real NOT NULL,
	transaction_iso_ts varchar(30) NOT NULL,
	transaction_note varchar(500),
	budget_item_id integer DEFAULT 0 NOT NULL,
	account_id integer DEFAULT 0 NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm real NOT NULL,
	create_iso_ts varchar(30) NOT NULL,
	updt_dt_tm real NOT NULL,
	updt_iso_ts varchar(30) NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
