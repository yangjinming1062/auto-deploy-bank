#!/bin/bash
#
# User Account Creation Script for Warehouse Management System
# This script creates admin and normal user accounts directly in the database
#

# Database configuration (adjust these values as needed)
DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-warehouse}"
DB_USER="${DB_USER:-root}"
DB_PASS="${DB_PASS:-123456}"

# Generate MD5 hash with salt
# Format: md5(md5(password + salt) + salt) with 2 iterations
generate_password_hash() {
    local password="$1"
    local salt="$2"
    # First hash: password + salt
    local first_hash=$(echo -n "${password}${salt}" | md5sum | awk '{print $1}')
    # Second hash with salt (simulating 2 iterations)
    echo -n "${first_hash}${salt}" | md5sum | awk '{print $1}'
}

# Generate UUID salt (uppercase)
generate_salt() {
    cat /proc/sys/kernel/random/uuid | tr '[:lower:]' '[:upper:]'
}

# Create admin user
create_admin_user() {
    local loginname="$1"
    local name="$2"
    local password="${3:-Admin@123}"

    local salt=$(generate_salt)
    local pwd_hash=$(generate_password_hash "$password" "$salt")

    echo "Creating admin user: $loginname"

    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" <<EOF
INSERT INTO sys_user (loginname, name, pwd, salt, type, available, ordernum, imgpath, deptid, leadername, address, remark, mgr)
VALUES ('$loginname', '$name', '$pwd_hash', '$salt', 0, 1, 100, '/images/defaultUserTitle.jpg', 1, '', '', 'Administrator account', 0);
EOF

    if [ $? -eq 0 ]; then
        echo "Admin user created successfully: $loginname / $password"
    else
        echo "Failed to create admin user: $loginname"
        return 1
    fi
}

# Create normal user
create_normal_user() {
    local loginname="$1"
    local name="$2"
    local password="${3:-User@123}"

    local salt=$(generate_salt)
    local pwd_hash=$(generate_password_hash "$password" "$salt")

    echo "Creating normal user: $loginname"

    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" <<EOF
INSERT INTO sys_user (loginname, name, pwd, salt, type, available, ordernum, imgpath, deptid, leadername, address, remark, mgr)
VALUES ('$loginname', '$name', '$pwd_hash', '$salt', 1, 1, 100, '/images/defaultUserTitle.jpg', 1, '', '', 'Normal user account', 0);
EOF

    if [ $? -eq 0 ]; then
        echo "Normal user created successfully: $loginname / $password"
    else
        echo "Failed to create normal user: $loginname"
        return 1
    fi
}

# Assign role to user
assign_role() {
    local user_id="$1"
    local role_id="$2"

    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" <<EOF
INSERT INTO sys_user_role (uid, roleid) VALUES ($user_id, $role_id);
EOF

    if [ $? -eq 0 ]; then
        echo "Role assigned successfully to user ID: $user_id"
    else
        echo "Failed to assign role to user ID: $user_id"
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "Warehouse Management System - User Account Creation"
    echo "=========================================="
    echo ""

    # Create admin user
    echo "--- Creating Admin Account ---"
    create_admin_user "admin" "System Administrator" "Admin@123"
    echo ""

    # Create normal user
    echo "--- Creating Normal User Account ---"
    create_normal_user "testuser" "Test User" "User@123"
    echo ""

    # Assign admin role to admin user (role ID 1 is typically admin)
    echo "--- Assigning Admin Role ---"
    # Get the admin user ID first
    admin_id=$(mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" -N -e "SELECT id FROM sys_user WHERE loginname='admin';" 2>/dev/null)
    if [ -n "$admin_id" ]; then
        assign_role "$admin_id" 1
    else
        echo "Warning: Could not find admin user to assign role"
    fi

    echo ""
    echo "=========================================="
    echo "Account creation completed!"
    echo ""
    echo "Login URL: /login/login"
    echo "Default Admin: admin / Admin@123"
    echo "Default User:  testuser / User@123"
    echo "=========================================="
}

main "$@"