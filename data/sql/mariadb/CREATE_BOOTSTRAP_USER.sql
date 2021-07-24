CREATE USER 'bootstrap'@'%';
ALTER USER 'bootstrap'@'%'
IDENTIFIED BY 'bootstrap' ;
GRANT Alter ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Create ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Create view ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Delete ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Delete history ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Drop ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Index ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Insert ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT References ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Select ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Show view ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Trigger ON BOOTSTRAP.* TO 'bootstrap'@'%';
GRANT Update ON BOOTSTRAP.* TO 'bootstrap'@'%';