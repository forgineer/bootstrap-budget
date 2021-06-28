/**
 * Name: INSERT_USER.sql
 * Purpose: Inserts new row into the USER table
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO "USER"
(last_name, first_name, middle_name, login, address_line_1, address_line_2, city, state, zipcode, email, phone_number, admin_ind, hash, salt, create_dt_tm, create_iso_ts, active_ind)
VALUES(?    /* last_name */
    , ?     /* first_name */
    , ?     /* middle_name */
    , ?     /* login */
    , ?     /* address_line_1 */
    , ?     /* address_line_2 */
    , ?     /* city */
    , ?     /* state */
    , ?     /* zipcode */
    , ?     /* email */
    , ?     /* phone_number */
    , ?     /* admin_ind */
    , ?     /* hash */
    , ?     /* salt */
    , ?     /* create_dt_tm */
    , ?     /* create_iso_ts */
    , ?);   /* active_ind */
