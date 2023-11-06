/**
 * Name: create_user.sql
 * Purpose: Creates a USER record.
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO USERS (
    last_name
    , first_name
    , middle_name
    , username
    , address_line_1
    , address_line_2
    , city
    , state
    , zipcode
    , email
    , phone_number
    , hash
    , salt
    , is_admin
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);