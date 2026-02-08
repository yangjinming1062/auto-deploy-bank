#!/bin/bash
# Account Creation Script for Spring Boot Application
# This script creates admin and normal user accounts via the registration API

set -e

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "Creating test accounts for security testing..."

# Function to register a user
register_user() {
    local username=$1
    local password=$2
    local email=$3

    echo "Registering user: $username"

    # Note: This script assumes the registration endpoint works without captcha
    # In production, you would need to handle email captcha verification

    curl -s -X POST "${BASE_URL}/register" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$username\",\"password\":\"$password\",\"email\":\"$email\",\"captcha\":\"123456\"}" \
        -w "\nHTTP Status: %{http_code}\n" || true

    echo ""
}

# Function to create admin user directly in database (bypassing registration)
create_admin_via_database() {
    local username=$1
    local password=$2
    local email=$3

    echo "Creating admin user directly in database: $username"

    # For H2 in-memory database, we connect via JDBC
    # This approach is used when the app is not running but we want to prepopulate
    # Since H2 is in-memory, this only works if the app is running

    if command -v curl &> /dev/null; then
        # Using HTTP to create user (if app is running)
        # The app auto-creates users on startup, so we might just need to set roles

        # For now, we'll use the register endpoint
        register_user "$username" "$password" "$email"
    fi
}

# Create admin account
echo "====================================="
echo "Creating Admin Account"
echo "====================================="
register_user "admin" "Admin@123" "admin@test.com"

# Create normal user account
echo "====================================="
echo "Creating Normal User Account"
echo "====================================="
register_user "testuser" "User@123" "user@test.com"

echo "====================================="
echo "Account creation completed!"
echo "====================================="
echo ""
echo "Admin Account:"
echo "  Username: admin"
echo "  Password: Admin@123"
echo "  Login URL: /login"
echo ""
echo "Normal User Account:"
echo "  Username: testuser"
echo "  Password: User@123"
echo "  Login URL: /login"
echo ""
echo "Note: The application also auto-creates these test accounts on startup:"
echo "  - zhangsan / zhangsan123"
echo "  - lisi / lisi123"
echo "  - wangwu / wangwu123"
echo "  - hello / hello123"
echo ""
echo "To log in, send a POST request to /login with:"
echo '  {"username":"admin", "password":"Admin@123", "captcha":"..."}'