/**
 * Name: INSERT_USER.sql
 * Purpose: Inserts into the USER table
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO "USER"
(last_name, first_name, middle_name, username, address_line_1, address_line_2, city, state, zipcode, email, phone_number, hash, salt, tutorial_ind, admin_ind, create_dt_tm, create_iso_ts, updt_dt_tm, updt_iso_ts, active_ind)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
