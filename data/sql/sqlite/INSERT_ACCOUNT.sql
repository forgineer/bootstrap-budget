/**
 * Name: INSERT_ACCOUNT.sql
 * Purpose: Inserts new row into the ACCOUNT table
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO ACCOUNT
(account_name, account_desc, account_nbr, route_nbr, user_id, create_dt_tm, create_iso_ts, active_ind)
VALUES(?, ?, ?, ?, ?, ?, ?, ?);