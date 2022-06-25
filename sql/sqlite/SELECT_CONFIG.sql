/**
 * Name: SELECT_CONFIG.sql
 * Purpose: Selects from the CONFIG table
 * Author: Blake Phillips (forgineer)
 */
SELECT config_id, config_text, config_value_int, config_value_flt, config_value_txt, config_value_set, user_id, create_dt_tm, create_iso_ts, updt_dt_tm, updt_iso_ts, active_ind
FROM CONFIG
/* Leaving out semicolon to allow more dynamic statements */