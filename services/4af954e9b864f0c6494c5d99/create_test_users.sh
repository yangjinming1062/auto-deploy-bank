#!/bin/bash
# Vikunja Test Account Creation Script
# This script creates admin and normal user accounts for security testing
#
# Usage: ./create_test_users.sh [admin_username] [admin_password] [normal_username] [normal_password]
# Or run without arguments to use default credentials

set -e

VIKUNJA_BIN="${VIKUNJA_BIN:-./vikunja}"

# Default credentials
ADMIN_USERNAME="${1:-admin}"
ADMIN_PASSWORD="${2:-Admin@123}"
NORMAL_USERNAME="${3:-testuser}"
NORMAL_PASSWORD="${4:-User@123}"

echo "=== Vikunja Test Account Creation ==="
echo ""

# Check if vikunja binary exists
if [ ! -f "$VIKUNJA_BIN" ]; then
    echo "Error: Vikunja binary not found at $VIKUNJA_BIN"
    echo "Please build the project first or set VIKUNJA_BIN environment variable"
    exit 1
fi

# Create admin user
echo "Creating admin user: $ADMIN_USERNAME"
$VIKUNJA_BIN user create \
    --username "$ADMIN_USERNAME" \
    --email "admin@test.local" \
    --password "$ADMIN_PASSWORD" \
    || echo "Admin user may already exist"

echo ""

# Create normal test user
echo "Creating normal user: $NORMAL_USERNAME"
$VIKUNJA_BIN user create \
    --username "$NORMAL_USERNAME" \
    --email "testuser@test.local" \
    --password "$NORMAL_PASSWORD" \
    || echo "Normal user may already exist"

echo ""
echo "=== Account Creation Complete ==="
echo ""
echo "Admin credentials:"
echo "  Username: $ADMIN_USERNAME"
echo "  Password: $ADMIN_PASSWORD"
echo "  Login URL: /api/v1/login"
echo ""
echo "Normal user credentials:"
echo "  Username: $NORMAL_USERNAME"
echo "  Password: $NORMAL_PASSWORD"
echo "  Login URL: /api/v1/login"
echo ""
echo "Note: All users in Vikunja have equal privileges by default."
echo "Use /api/v1/register for self-registration if enabled."
