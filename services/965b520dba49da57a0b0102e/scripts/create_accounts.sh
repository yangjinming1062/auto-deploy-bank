#!/bin/bash

# LifePhoton Account Creation Script
# Creates admin and normal user accounts directly in the database
# Usage: ./create_accounts.sh [db_host] [db_port] [db_name] [db_user] [db_pass]

set -e

# Configuration with defaults
DB_HOST="${1:-127.0.0.1}"
DB_PORT="${2:-5432}"
DB_NAME="${3:-lifephoton}"
DB_USER="${4:-postgres}"
DB_PASS="${5:-123456}"

# Credentials to create
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="Admin@123"
ADMIN_EMAIL="admin@lifephoton.local"

NORMAL_USERNAME="testuser"
NORMAL_PASSWORD="User@123"
NORMAL_EMAIL="testuser@lifephoton.local"

echo "Creating LifePhoton accounts..."
echo "Database: $DB_HOST:$DB_PORT/$DB_NAME"

# Function to generate random token
generate_token() {
    head -c 32 /dev/urandom | md5sum | head -c 32
}

ADMIN_ACCESS_TOKEN=$(generate_token)
ADMIN_REFRESH_TOKEN=$(generate_token)
USER_ACCESS_TOKEN=$(generate_token)
USER_REFRESH_TOKEN=$(generate_token)

# SQL to insert admin user
ADMIN_SQL="INSERT INTO user_data (avatar, username, email, password, access_token, refresh_token, \"group\", permissions, data)
VALUES (
    '',
    '$ADMIN_USERNAME',
    '$ADMIN_EMAIL',
    '$ADMIN_PASSWORD',
    '$ADMIN_ACCESS_TOKEN',
    '$ADMIN_REFRESH_TOKEN',
    'admin',
    '[\"admin.*\", \"default.*\"]'::jsonb,
    '{}'::jsonb
)
ON CONFLICT (username) DO UPDATE SET
    password = EXCLUDED.password,
    email = EXCLUDED.email,
    access_token = EXCLUDED.access_token,
    refresh_token = EXCLUDED.refresh_token,
    \"group\" = EXCLUDED.\"group\",
    permissions = EXCLUDED.permissions;"

# SQL to insert normal user
USER_SQL="INSERT INTO user_data (avatar, username, email, password, access_token, refresh_token, \"group\", permissions, data)
VALUES (
    '',
    '$NORMAL_USERNAME',
    '$NORMAL_EMAIL',
    '$NORMAL_PASSWORD',
    '$USER_ACCESS_TOKEN',
    '$USER_REFRESH_TOKEN',
    'default',
    '[\"default.*\"]'::jsonb,
    '{}'::jsonb
)
ON CONFLICT (username) DO UPDATE SET
    password = EXCLUDED.password,
    email = EXCLUDED.email,
    access_token = EXCLUDED.access_token,
    refresh_token = EXCLUDED.refresh_token,
    permissions = EXCLUDED.permissions;"

export PGPASSWORD="$DB_PASS"

# Create admin user
echo "Creating admin user: $ADMIN_USERNAME"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$ADMIN_SQL" 2>/dev/null || {
    echo "Failed to create admin user. Make sure PostgreSQL is running and the database exists."
    exit 1
}

# Create normal user
echo "Creating normal user: $NORMAL_USERNAME"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$USER_SQL" 2>/dev/null || {
    echo "Failed to create normal user."
    exit 1
}

echo ""
echo "Accounts created successfully!"
echo ""
echo "Admin Account:"
echo "  Username: $ADMIN_USERNAME"
echo "  Password: $ADMIN_PASSWORD"
echo "  Email: $ADMIN_EMAIL"
echo "  Group: admin (full privileges)"
echo ""
echo "Normal User Account:"
echo "  Username: $NORMAL_USERNAME"
echo "  Password: $NORMAL_PASSWORD"
echo "  Email: $NORMAL_EMAIL"
echo "  Group: default (standard privileges)"
echo ""
echo "Login endpoint: POST /login"
echo "Request body: {\"username\": \"<username>\", \"password\": \"<password>\"}"