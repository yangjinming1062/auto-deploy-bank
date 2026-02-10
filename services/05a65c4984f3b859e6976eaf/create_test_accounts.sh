#!/bin/bash
# Quarkus File-Based Authentication - Account Creation Script
# This script adds test accounts to the properties-based security configuration

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USERS_FILE="${SCRIPT_DIR}/src/main/resources/test-users.properties"
ROLES_FILE="${SCRIPT_DIR}/src/main/resources/test-roles.properties"

echo "Creating test accounts for Quarkus application..."

# Create admin account
echo "admin=Admin@123" >> "$USERS_FILE"
echo "admin=admin,user,manager" >> "$ROLES_FILE"
echo "Created admin account: admin / Admin@123"

# Create normal user account
echo "user=User@123" >> "$USERS_FILE"
echo "user=user" >> "$ROLES_FILE"
echo "Created normal user account: user / User@123"

echo "Test accounts created successfully!"
echo ""
echo "Note: The application must be restarted for changes to take effect."