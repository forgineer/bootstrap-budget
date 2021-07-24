/**
 * Name: CREATE_ACCOUNT_TABLE.sql
 * Purpose: Creates the ACCOUNT table
 * Author: Blake Phillips (forgineer)
 */
CREATE TABLE BOOTSTRAP.ACCOUNT (
	account_id INT auto_increment NOT NULL,
	account_name varchar(100) NOT NULL,
	account_desc varchar(500) NULL,
	account_nbr varchar(50) NULL,
	account_route_nbr varchar(50) NULL,
	account_open_amt DOUBLE DEFAULT 0 NOT NULL,
	account_est_amt DOUBLE NULL,
	budget_id INT NOT NULL,
	user_id INT NOT NULL,
	create_dt_tm DOUBLE NOT NULL,
	create_iso_ts varchar(30) NOT NULL,
	updt_dt_tm DOUBLE NOT NULL,
	updt_iso_ts varchar(30) NOT NULL,
	active_ind TINYINT DEFAULT 1 NOT NULL,
	CONSTRAINT ACCOUNT_pk PRIMARY KEY (account_id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;
