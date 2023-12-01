-- Check if the user exists
SELECT user, host FROM mysql.user WHERE user = 'auth_user' AND host = 'localhost';

-- Drop the user if it exists
DROP USER IF EXISTS 'auth_user'@'localhost';

-- Create User
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';

-- Create Database
CREATE DATABASE auth;

-- Grant Privileges
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- Switch to the 'auth' Database
USE auth;

-- Create Table
CREATE TABLE `user` (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insert Data
INSERT INTO `user` (email, password) VALUES ('xyz@gmail.com', 'Admin123');
