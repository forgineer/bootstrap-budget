/**
 * Name: postgresql_schema.sql
 * Purpose: Creates the Bootstrap Budget table schema for SQLite
 * Author: Blake Phillips (forgineer)
 */
DROP TABLE IF EXISTS CONFIG;
DROP TABLE IF EXISTS DASHBOARD;
DROP TABLE IF EXISTS TRANSACTIONS;
DROP TABLE IF EXISTS USER_BUDGET;
DROP TABLE IF EXISTS ACCOUNT;
DROP TABLE IF EXISTS BUDGET_ITEM;
DROP TABLE IF EXISTS BUDGET;
DROP TABLE IF EXISTS USERS;

CREATE TABLE USERS (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	last_name TEXT NOT NULL,
	first_name TEXT NOT NULL,
	middle_name TEXT,
	username TEXT UNIQUE NOT NULL,
	address_line_1 TEXT,
	address_line_2 TEXT,
	city TEXT,
	state TEXT,
	zipcode TEXT,
	email TEXT,
	phone_number TEXT,
	hash TEXT NOT NULL,
	salt TEXT NOT NULL,
	tutorial_ind INTEGER DEFAULT 1,
	admin_ind INTEGER DEFAULT 0 NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL
);

CREATE TABLE CONFIG (
	config_id INTEGER PRIMARY KEY AUTOINCREMENT,
	config_text TEXT NOT NULL,
	config_value_int INTEGER,
	config_value_flt REAL,
	config_value_txt TEXT,
	config_value_set INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES USERS (user_id)
);

CREATE TABLE BUDGET (
	budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
	budget_name TEXT UNIQUE NOT NULL,
	budget_desc TEXT,
	budget_year INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES USERS (user_id)
);

CREATE TABLE USER_BUDGET (
	user_budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	permissions INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (budget_id) REFERENCES BUDGET (budget_id),
	FOREIGN KEY (user_id) REFERENCES USERS (user_id)
);

CREATE TABLE BUDGET_ITEM (
	budget_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
	budget_id INTEGER NOT NULL,
	budget_item_name TEXT UNIQUE NOT NULL,
	budget_item_desc TEXT,
	budget_item_amt REAL DEFAULT 0.0 NOT NULL,
	budget_item_seq INTEGER DEFAULT 99 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (budget_id) REFERENCES BUDGET (budget_id),
	FOREIGN KEY (user_id) REFERENCES USERS (user_id)
);

CREATE TABLE DASHBOARD (
	dashboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
	dashboard_year INTEGER NOT NULL,
	dashboard_month INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	budget_item_id INTEGER NOT NULL,
	budget_item_amt REAL DEFAULT 0.0 NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (budget_id) REFERENCES BUDGET (budget_id),
	FOREIGN KEY (budget_item_id) REFERENCES BUDGET_ITEM (budget_item_id)
);

CREATE TABLE ACCOUNT (
	account_id INTEGER PRIMARY KEY AUTOINCREMENT,
	account_name TEXT UNIQUE NOT NULL,
	account_desc TEXT,
	account_nbr TEXT,
	account_route_nbr TEXT,
	account_open_amt REAL DEFAULT 0.0 NOT NULL,
	account_est_amt REAL,
	budget_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (budget_id) REFERENCES BUDGET (budget_id),
	FOREIGN KEY (user_id) REFERENCES USERS (user_id)

);

CREATE TABLE TRANSACTIONS (
	transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
	transaction_desc TEXT,
	transaction_norm TEXT,
	transaction_amt REAL DEFAULT 0.0 NOT NULL,
	transaction_year INTEGER NOT NULL,
	transaction_month INTEGER NOT NULL,
	transaction_dt_tm timestamp NOT NULL,
	transaction_note TEXT,
	budget_item_id INTEGER DEFAULT 0 NOT NULL,
	account_id INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	active_ind INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (account_id) REFERENCES ACCOUNT (account_id),
	FOREIGN KEY (budget_item_id) REFERENCES BUDGET_ITEM (budget_item_id),
	FOREIGN KEY (user_id) REFERENCES USERS (user_id)
);
