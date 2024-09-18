-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS ub_db;
CREATE USER IF NOT EXISTS 'ub_dev'@'localhost' IDENTIFIED BY 'ub_pwd';
GRANT ALL PRIVILEGES ON `ub_db`.* TO 'ub_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ub_dev'@'localhost';
FLUSH PRIVILEGES;
