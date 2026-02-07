-- Spring Boot Test User Creation Script
-- Creates admin and normal user accounts for security testing
-- Execute against your application database

-- Create admin user (full privileges)
INSERT INTO users (username, password, enabled) VALUES ('admin', '{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG', true);
INSERT INTO authorities (username, authority) VALUES ('admin', 'ROLE_ADMIN');
INSERT INTO authorities (username, authority) VALUES ('admin', 'ROLE_USER');

-- Create normal user (standard privileges)
INSERT INTO users (username, password, enabled) VALUES ('testuser', '{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG', true);
INSERT INTO authorities (username, authority) VALUES ('testuser', 'ROLE_USER');

-- If using JdbcUserDetailsManager schema (default Spring Security tables)
-- The above assumes a schema like:
-- CREATE TABLE users (username VARCHAR(50) NOT NULL PRIMARY KEY, password VARCHAR(500) NOT NULL, enabled BOOLEAN NOT NULL);
-- CREATE TABLE authorities (username VARCHAR(50) NOT NULL, authority VARCHAR(50) NOT NULL, FOREIGN KEY (username) REFERENCES users(username));