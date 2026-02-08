-- Account Creation Script for Spring Boot Demo Application
-- This script adds test users to the H2 in-memory database
-- Password is 'Admin@123' (BCrypt encoded) for admin user
-- Password is 'User@123' (BCrypt encoded) for normal user

-- Create admin user (username: admin, password: Admin@123)
INSERT INTO users (username, password, enabled) VALUES ('admin', '{bcrypt}$2b$12$ViQ7ESQ0G3AdFdcHaMc1x.GUL8pPp2ljTzuNAbO1IgbF8BFkiTMRW', true);
INSERT INTO authorities (username, authority) VALUES ('admin', 'ROLE_ADMIN');
INSERT INTO authorities (username, authority) VALUES ('admin', 'ROLE_USER');

-- Create normal user (username: testuser, password: User@123)
INSERT INTO users (username, password, enabled) VALUES ('testuser', '{bcrypt}$2b$12$TDxruWAml2ErIQyVixazBOtePuYhq5xbH.vxr23YfdUcBHD9gW55a', true);
INSERT INTO authorities (username, authority) VALUES ('testuser', 'ROLE_USER');