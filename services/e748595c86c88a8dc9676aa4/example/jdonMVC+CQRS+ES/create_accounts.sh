#!/bin/bash
# Account creation script for JdonFramework example application
# Creates admin and normal user accounts in the testuser table

# Database configuration - can be overridden via environment variables
DB_URL="${DB_URL:-jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8}"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-}"

# Test account credentials
ADMIN_USER="admin"
ADMIN_PASS="Admin@123"
NORMAL_USER="user1"
NORMAL_PASS="User@123"

echo "Creating test accounts in database: $DB_URL"

# Check if mysql client is available
if command -v mysql &> /dev/null; then
    mysql -h "${DB_URL##*://}" -P "${DB_URL##*:3306/}" -u "$DB_USER" -p"$DB_PASSWORD" test 2>/dev/null << EOF
INSERT INTO testuser (userId, name, password, email, roleName)
VALUES ('admin', 'Administrator', '$ADMIN_PASS', 'admin@test.com', 'admin')
ON DUPLICATE KEY UPDATE name='Administrator', password='$ADMIN_PASS', roleName='admin';

INSERT INTO testuser (userId, name, password, email, roleName)
VALUES ('$NORMAL_USER', 'Normal User', '$NORMAL_PASS', 'user@test.com', 'user')
ON DUPLICATE KEY UPDATE name='Normal User', password='$NORMAL_PASS', roleName='user';
EOF
    echo "Test accounts created successfully!"
    echo "Admin: $ADMIN_USER / $ADMIN_PASS"
    echo "User:  $NORMAL_USER / $NORMAL_PASS"
else
    echo "MySQL client not found. Please run create_test_accounts.java with JDBC driver."
    echo "Compile and run: javac create_test_accounts.java && java create_test_accounts"
fi