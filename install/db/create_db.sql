CREATE USER bible WITH password '123456';
ALTER USER bible CREATEDB;
CREATE DATABASE bible;
GRANT ALL privileges ON DATABASE bible TO bible;