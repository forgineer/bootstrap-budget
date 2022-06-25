/**
 * Name: CREATE_ACCOUNT_TABLE.sql
 * Purpose: Creates the ACCOUNT table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE ACCOUNT (
	account_id serial NOT NULL PRIMARY KEY,
	account_name varchar(100) NOT NULL,
	account_desc varchar(500),
	account_nbr varchar(50),
	account_route_nbr varchar(50),
	account_open_amt real DEFAULT 0 NOT NULL,
	account_est_amt real,
	budget_id integer NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm real NOT NULL,
	updt_dt_tm real NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
