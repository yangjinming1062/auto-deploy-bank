#!/bin/bash
# Script to create test user accounts for the Elkeid RASP Manager
# Usage: ./create_test_users.sh <config_path> <admin_password> <normal_password>
# Example: ./create_test_users.sh ./conf/svr.yml Admin@123 User@123

set -e

CONFIG_PATH="${1:-./conf/svr.yml}"
ADMIN_PASS="${2:-Admin@123}"
NORMAL_PASS="${2:-User@123}"

cd /home/ubuntu/deploy-projects/18c55c0a992a1a4ea12094ed/server/manager

echo "Building init tools..."
cd cmd/inittools && go build -o ../../bin/init . && cd ../..

echo "Creating admin user..."
./bin/init -c "$CONFIG_PATH" -t addUser -u admin -p "$ADMIN_PASS"

echo "Creating normal user..."
./bin/init -c "$CONFIG_PATH" -t addUser -u normal -p "$NORMAL_PASS"

echo "Test users created successfully:"
echo "  admin:  password = $ADMIN_PASS  (level 0 - admin)"
echo "  normal: password = $NORMAL_PASS  (level 3 - agent readonly)"