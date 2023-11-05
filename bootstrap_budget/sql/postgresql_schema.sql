/**
 * Name: postgresql_schema.sql
 * Purpose: Creates the Bootstrap Budget table schema for PostgreSQL
 * Author: Blake Phillips (forgineer)
 */
DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS dashboard;
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS user_budget;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS budget_item;
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS users;

CREATE TABLE ACCOUNT (
	account_id serial NOT NULL PRIMARY KEY,
	account_name varchar(100) UNIQUE NOT NULL,
	account_desc varchar(500),
	account_nbr varchar(50),
	account_route_nbr varchar(50),
	account_open_amt real DEFAULT 0.0 NOT NULL,
	account_est_amt real,
	budget_id integer NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

CREATE TABLE BUDGET_ITEM (
	budget_item_id serial NOT NULL PRIMARY KEY,
	budget_id integer NOT NULL,
	budget_item_name varchar(100) UNIQUE NOT NULL,
	budget_item_desc varchar(200),
	budget_item_amt real DEFAULT 0.0 NOT NULL,
	budget_item_seq integer DEFAULT 99 NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

CREATE TABLE BUDGET (
	budget_id serial NOT NULL PRIMARY KEY,
	budget_name varchar(100) UNIQUE NOT NULL,
	budget_desc varchar(200),
	budget_year integer NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

CREATE TABLE CONFIG (
	config_id serial NOT NULL PRIMARY KEY,
	config_text varchar(100) NOT NULL,
	config_value_int integer,
	config_value_flt real,
	config_value_txt varchar(100),
	config_value_set integer DEFAULT 0 NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

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

CREATE TABLE TRANSACTION (
	transaction_id serial NOT NULL PRIMARY KEY,
	transaction_desc varchar(200),
	transaction_norm varchar(200),
	transaction_amt real DEFAULT 0.0 NOT NULL,
	transaction_year integer NOT NULL,
	transaction_month integer NOT NULL,
	transaction_dt_tm timestamp NOT NULL,
	transaction_note varchar(500),
	budget_item_id integer DEFAULT 0 NOT NULL,
	account_id integer DEFAULT 0 NOT NULL,
	user_id integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

CREATE TABLE USER_BUDGET (
	user_budget_id serial NOT NULL PRIMARY KEY,
	user_id integer NOT NULL,
	budget_id integer NOT NULL,
	permissions integer NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

CREATE TABLE USERS (
	user_id serial NOT NULL PRIMARY KEY,
	last_name varchar(100) NOT NULL,
	first_name varchar(100) NOT NULL,
	middle_name varchar(100),
	username varchar(40) UNIQUE NOT NULL,
	address_line_1 varchar(100),
	address_line_2 varchar(100),
	city varchar(100),
	state varchar(50),
	zipcode varchar(20),
	email varchar(100),
	phone_number varchar(10),
	hash varchar(100) NOT NULL,
	salt varchar(100) NOT NULL,
	tutorial_ind integer DEFAULT 1,
	admin_ind integer DEFAULT 0 NOT NULL,
	create_dt_tm timestamp NOT NULL,
	updt_dt_tm timestamp NOT NULL,
	active_ind integer DEFAULT 1 NOT NULL
);

ALTER TABLE public.config ADD CONSTRAINT config_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.account ADD CONSTRAINT account_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.account ADD CONSTRAINT account_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.budget ADD CONSTRAINT budget_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.budget_item ADD CONSTRAINT budget_item_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.budget_item ADD CONSTRAINT budget_item_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.dashboard ADD CONSTRAINT dashboard_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.dashboard ADD CONSTRAINT dashboard_fk_1 FOREIGN KEY (budget_item_id) REFERENCES public.budget_item(budget_item_id);

ALTER TABLE public."transaction" ADD CONSTRAINT transaction_fk FOREIGN KEY (account_id) REFERENCES public.account(account_id);
ALTER TABLE public."transaction" ADD CONSTRAINT transaction_fk_1 FOREIGN KEY (budget_item_id) REFERENCES public.budget_item(budget_item_id);
ALTER TABLE public."transaction" ADD CONSTRAINT transaction_fk_2 FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.user_budget ADD CONSTRAINT user_budget_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.user_budget ADD CONSTRAINT user_budget_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);
