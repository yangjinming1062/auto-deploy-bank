#!/bin/bash
# Open Liberty User Account Creation Script
# This script adds new users to the server.xml basicRegistry

SERVER_XML="${1:-server.xml}"
USERNAME="${2:-}"
PASSWORD="${3:-}"
ROLE="${4:-user}"

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
    echo "Usage: $0 <server.xml> <username> <password> [role: admin|user]"
    echo "Example: $0 server.xml newuser Pass@123 admin"
    exit 1
fi

if [ ! -f "$SERVER_XML" ]; then
    echo "Error: $SERVER_XML not found"
    exit 1
fi

# Check if user already exists
if grep -q "name=\"$USERNAME\"" "$SERVER_XML"; then
    echo "User '$USERNAME' already exists in $SERVER_XML"
    exit 1
fi

# Find the closing </basicRegistry> tag and insert before it
if [ "$ROLE" = "admin" ]; then
    # Insert as admin user (can add admin-specific groups if needed)
    sed -i "/<\/basicRegistry>/i\\        <user name=\"$USERNAME\" password=\"$PASSWORD\" />" "$SERVER_XML"
else
    # Insert as regular user
    sed -i "/<\/basicRegistry>/i\\        <user name=\"$USERNAME\" password=\"$PASSWORD\" />" "$SERVER_XML"
fi

echo "User '$USERNAME' added successfully with $ROLE role"
echo "Restart the server for changes to take effect"