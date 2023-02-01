-- This scripts will create the user for Django to access the database resources 

-- For Developer Machines
CREATE DATABASE evoting;
GRANT USAGE on *.* to 'evoting_django'@'localhost' IDENTIFIED BY 'django_password';
GRANT ALL PRIVILEGES ON evoting.* to 'evoting_django'@'localhost';

-- For Deployment Machines
CREATE DATABASE evoting;
GRANT USAGE on *.* to 'evoting_django'@'192.168.0.1' IDENTIFIED BY 'django_password';
GRANT ALL PRIVILEGES ON evoting.* to 'evoting_django'@'192.168.0.1';