/**
 * Name: postgresql_schema.sql
 * Purpose: Creates the Bootstrap Budget table schema for PostgreSQL.
 * Author: Blake Phillips (forgineer)
 */
DROP TABLE IF EXISTS CONFIG;
--
DROP TABLE IF EXISTS DASHBOARD;
--
DROP TABLE IF EXISTS TRANSACTIONS;
--
DROP TABLE IF EXISTS USER_BUDGET;
--
DROP TABLE IF EXISTS ACCOUNT;
--
DROP TABLE IF EXISTS BUDGET_ITEM;
--
DROP TABLE IF EXISTS BUDGET;
--
DROP TABLE IF EXISTS USERS;
--
CREATE TABLE ACCOUNT (
	account_id SERIAL NOT NULL PRIMARY KEY,
	account_name VARCHAR(100) UNIQUE NOT NULL,
	account_desc VARCHAR(500),
	account_nbr VARCHAR(50),
	account_route_nbr VARCHAR(50),
	account_open_amt REAL DEFAULT 0.0 NOT NULL,
	account_est_amt REAL,
	budget_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE BUDGET_ITEM (
	budget_item_id serial NOT NULL PRIMARY KEY,
	budget_id INTEGER NOT NULL,
	budget_item_name VARCHAR(100) UNIQUE NOT NULL,
	budget_item_desc VARCHAR(200),
	budget_item_amt REAL DEFAULT 0.0 NOT NULL,
	budget_item_seq INTEGER DEFAULT 99 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE BUDGET (
	budget_id serial NOT NULL PRIMARY KEY,
	budget_name VARCHAR(100) UNIQUE NOT NULL,
	budget_desc VARCHAR(200),
	budget_year INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE CONFIG (
	config_id serial NOT NULL PRIMARY KEY,
	config_text VARCHAR(100) NOT NULL,
	config_value_int INTEGER,
	config_value_flt REAL,
	config_value_txt VARCHAR(100),
	config_value_set INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE DASHBOARD (
	dashboard_id serial NOT NULL PRIMARY KEY,
	dashboard_year INTEGER NOT NULL,
	dashboard_month INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	budget_item_id INTEGER NOT NULL,
	budget_item_amt REAL DEFAULT 0.0 NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE TRANSACTIONS (
	transaction_id serial NOT NULL PRIMARY KEY,
	transaction_desc VARCHAR(200),
	transaction_norm VARCHAR(200),
	transaction_amt REAL DEFAULT 0.0 NOT NULL,
	transaction_dt_tm TIMESTAMP NOT NULL,
	transaction_year INTEGER GENERATED ALWAYS AS (DATE_PART('year', transaction_dt_tm)) VIRTUAL NOT NULL,
    transaction_month INTEGER GENERATED ALWAYS AS (DATE_PART('year', transaction_dt_tm)) VIRTUAL NOT NULL,
    transaction_day INTEGER GENERATED ALWAYS AS (DATE_PART('month', transaction_dt_tm)) VIRTUAL NOT NULL,
	transaction_note VARCHAR(500),
	budget_item_id INTEGER DEFAULT 0 NOT NULL,
	account_id INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE USER_BUDGET (
	user_budget_id serial NOT NULL PRIMARY KEY,
	user_id INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	permissions INTEGER NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
CREATE TABLE USERS (
	user_id serial NOT NULL PRIMARY KEY,
	last_name VARCHAR(100),
	first_name VARCHAR(100),
	middle_name VARCHAR(100),
	username VARCHAR(40) UNIQUE NOT NULL,
	address_line_1 VARCHAR(100),
	address_line_2 VARCHAR(100),
	city VARCHAR(100),
	state VARCHAR(50),
	zipcode VARCHAR(20),
	email VARCHAR(100),
	phone_number VARCHAR(10),
	hash TEXT NOT NULL,
	salt TEXT NOT NULL,
	is_admin BOOLEAN DEFAULT 0 NOT NULL,
	created_dt_tm TIMESTAMP NOT NULL,
	updated_dt_tm TIMESTAMP NOT NULL,
	is_active BOOLEAN DEFAULT 1 NOT NULL
);
--
ALTER TABLE public.config ADD CONSTRAINT config_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id);
--
ALTER TABLE public.account ADD CONSTRAINT account_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
--
ALTER TABLE public.account ADD CONSTRAINT account_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);
--
ALTER TABLE public.budget ADD CONSTRAINT budget_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id);
--
ALTER TABLE public.budget_item ADD CONSTRAINT budget_item_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
--
ALTER TABLE public.budget_item ADD CONSTRAINT budget_item_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);
--
ALTER TABLE public.dashboard ADD CONSTRAINT dashboard_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
--
ALTER TABLE public.dashboard ADD CONSTRAINT dashboard_fk_1 FOREIGN KEY (budget_item_id) REFERENCES public.budget_item(budget_item_id);
--
ALTER TABLE public.transactions ADD CONSTRAINT transactions_fk FOREIGN KEY (account_id) REFERENCES public.account(account_id);
--
ALTER TABLE public.transactions ADD CONSTRAINT transactions_fk_1 FOREIGN KEY (budget_item_id) REFERENCES public.budget_item(budget_item_id);
--
ALTER TABLE public.transactions ADD CONSTRAINT transactions_fk_2 FOREIGN KEY (user_id) REFERENCES public.users(user_id);
--
ALTER TABLE public.user_budget ADD CONSTRAINT user_budget_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
--
ALTER TABLE public.user_budget ADD CONSTRAINT user_budget_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);
