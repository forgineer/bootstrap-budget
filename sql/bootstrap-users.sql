-- As ROOT...
-- SELECT USER FROM mysql.user;
CREATE USER bootstrap IDENTIFIED BY 'budg3tm@ster';
-- Grant bootstrap access to the bootstrap database, it's tables and routines
GRANT SELECT, INSERT, UPDATE ON bootstrap.* TO bootstrap;
-- SHOW GRANTS FOR bootstrap;
-- REVOKE DELETE ON bootstrap.* FROM bootstrap;


CREATE USER bootstrap_ops IDENTIFIED BY 'budg3t0ps';
-- Grant bootstrap access to the bootstrap database, it's tables and routines
GRANT SELECT, INSERT, UPDATE, DELETE ON bootstrap.* TO bootstrap_ops;
-- SHOW GRANTS FOR bootstrap_ops;


-- Grant blake all access to the bootstrap database, it's tables and routines
GRANT SELECT, INSERT, UPDATE, DELETE ON bootstrap.* TO blake;
GRANT ALL ON bootstrap.* TO blake;