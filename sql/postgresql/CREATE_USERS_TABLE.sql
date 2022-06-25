/**
 * Name: CREATE_USERS_TABLE.sql
 * Purpose: Creates the USERS table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE USERS (
	user_id serial NOT NULL PRIMARY KEY,
	last_name varchar(100) NOT NULL,
	first_name varchar(100) NOT NULL,
	middle_name varchar(100),
	username varchar(40) NOT NULL,
	address_line_1 varchar(100),
	address_line_2 varchar(100),
	city varchar(100),
	state varchar(50),
	zipcode varchar(20),
	email varchar(100),
	phone_number varchar(10),
	hash varchar(100),
	salt varchar(100),
	tutorial_ind integer DEFAULT 1,
	admin_ind integer DEFAULT 0 NOT NULL,
	create_dt_tm real NOT NULL,
	create_iso_ts varchar(30) NOT NULL,
	updt_dt_tm real NOT NULL,
	updt_iso_ts varchar(30) NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);
