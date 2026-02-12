#!/bin/bash
# Account Creation Script for Quarkus Application
# This script creates admin and normal user accounts in the file-based security realm

USERS_FILE="src/main/resources/test-users.properties"
ROLES_FILE="src/main/resources/test-roles.properties"

# Admin account credentials
ADMIN_USER="admin"
ADMIN_PASS="Admin@123"
ADMIN_ROLES="admin,user,manager"

# Normal user account credentials
NORMAL_USER="user"
NORMAL_PASS="User@123"
NORMAL_ROLES="user"

# Function to add user to users file
add_user() {
    local username=$1
    local password=$2
    local roles=$3

    # Check if user already exists
    if grep -q "^${username}=" "$USERS_FILE" 2>/dev/null; then
        echo "User '$username' already exists in $USERS_FILE"
        return 1
    fi

    # Add to users file
    echo "${username}=${password}" >> "$USERS_FILE"
    echo "Added user '$username' to $USERS_FILE"

    # Add to roles file
    echo "${username}=${roles}" >> "$ROLES_FILE"
    echo "Added roles for '$username' to $ROLES_FILE"

    return 0
}

echo "=== Quarkus Account Creation Script ==="
echo ""

# Create admin account
echo "Creating admin account..."
add_user "$ADMIN_USER" "$ADMIN_PASS" "$ADMIN_ROLES"
echo ""

# Create normal user account
echo "Creating normal user account..."
add_user "$NORMAL_USER" "$NORMAL_PASS" "$NORMAL_ROLES"
echo ""

echo "=== Account Creation Complete ==="
echo "Admin user: $ADMIN_USER / $ADMIN_PASS (roles: $ADMIN_ROLES)"
echo "Normal user: $NORMAL_USER / $NORMAL_PASS (roles: $NORMAL_ROLES)"
echo ""
echo "Restart the application to apply changes."