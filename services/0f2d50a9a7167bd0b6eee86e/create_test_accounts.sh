#!/bin/bash
# Account creation script for Lowcoder (Spring Boot application)
# This script creates admin and normal user accounts via the form login/register API

API_BASE_URL="${API_BASE_URL:-http://localhost:8080}"

echo "Creating test accounts for Lowcoder..."

# Function to create user (register or login)
create_user() {
    local username=$1
    local password=$2
    local register=$3  # "true" to register, "false" to login

    response=$(curl -s -X POST "${API_BASE_URL}/api/auth/form/login" \
        -H "Content-Type: application/json" \
        -d '{
            "loginId": "'"${username}"'",
            "password": "'"${password}"'",
            "register": '"${register}"',
            "source": "EMAIL",
            "authId": ""
        }')

    echo "Response for ${username} (register=${register}): ${response}"
}

# Create admin account (register=true to create new user)
echo "Creating admin account..."
create_user "admin@lowcoder.org" "Admin@123" "true"

# Create normal user account (register=true to create new user)
echo ""
echo "Creating normal user account..."
create_user "user@lowcoder.org" "User@123" "true"

echo ""
echo "Account creation completed!"
echo ""
echo "Note: Admin can create additional users via the admin panel or by inviting users."