/**
 * Name: UPDATE_ACCOUNT.sql
 * Purpose: Updates a row on the ACCOUNT table
 * Author: Blake Phillips (forgineer)
 */
UPDATE ACCOUNT
SET account_name=?, account_desc=?, account_nbr=?, route_nbr=?, user_id=?, create_dt_tm=?, create_iso_ts=?, active_ind=?
WHERE account_id=?;
