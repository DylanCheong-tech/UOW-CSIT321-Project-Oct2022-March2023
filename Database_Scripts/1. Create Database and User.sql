-- This scripts will create the user for Django to access the database resources 

CREATE DATABASE evoting;
GRANT USAGE on *.* to 'evoting_django'@'localhost' IDENTIFIED BY 'django_password';
GRANT ALL PRIVILEGES ON evoting.* to 'evoting_django'@'localhost';