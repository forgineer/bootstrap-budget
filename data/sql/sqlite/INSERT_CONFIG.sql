/**
 * Name: INSERT_CONFIG.sql
 * Purpose: Inserts into the CONFIG table
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO CONFIG
(config_text, config_value_int, config_value_flt, config_value_txt, config_value_set, user_id, create_dt_tm, create_iso_ts, updt_dt_tm, updt_iso_ts, active_ind)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
