#!/bin/bash
#
# Quarkus User Account Creation Script
# This script demonstrates how to create user accounts for a Quarkus application
# using the file-based security realm.
#
# Usage: ./create-users.sh <username> <password> <roles>
# Example: ./create-users.sh admin Admin@123 admin,user
#

set -e

USERS_FILE="src/main/resources/test-users.properties"
ROLES_FILE="src/main/resources/test-roles.properties"
APP_PROPS="src/main/resources/application.properties"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Quarkus User Account Creation Script"
echo "=========================================="

if [ $# -lt 3 ]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo ""
    echo "Usage: $0 <username> <password> <roles>"
    echo ""
    echo "Arguments:"
    echo "  username  - The username for the new account"
    echo "  password  - The password for the new account"
    echo "  roles     - Comma-separated list of roles (e.g., admin,user)"
    echo ""
    echo "Examples:"
    echo "  $0 admin Admin@123 admin,user"
    echo "  $0 john Secret123 user"
    echo ""
    exit 1
fi

USERNAME="$1"
PASSWORD="$2"
ROLES="$3"

# Validate username (alphanumeric and underscores only)
if ! [[ "$USERNAME" =~ ^[a-zA-Z0-9_]+$ ]]; then
    echo -e "${RED}Error: Username must contain only alphanumeric characters and underscores${NC}"
    exit 1
fi

# Check if user already exists in users file
if grep -q "^${USERNAME}=" "$USERS_FILE" 2>/dev/null; then
    echo -e "${YELLOW}Warning: User '$USERNAME' already exists in users file${NC}"
    read -p "Do you want to update the existing user? (y/n): " -n 1 -r
    echo
    if ! [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Add/Update user to users file
echo "Adding/updating user '$USERNAME' in $USERS_FILE..."
if [ -f "$USERS_FILE" ]; then
    # Remove existing entry for this user
    sed -i "/^${USERNAME}=.*$/d" "$USERS_FILE"
fi

# Add new user entry
echo "${USERNAME}=${PASSWORD}" >> "$USERS_FILE"
echo -e "${GREEN}User added to users file${NC}"

# Add/Update roles in roles file
echo "Assigning roles '$ROLES' to user '$USERNAME' in $ROLES_FILE..."
if [ -f "$ROLES_FILE" ]; then
    # Remove existing entry for this user
    sed -i "/^${USERNAME}=.*$/d" "$ROLES_FILE"
fi

# Add new roles entry
echo "${USERNAME}=${ROLES}" >> "$ROLES_FILE"
echo -e "${GREEN}Roles assigned${NC}"

echo ""
echo "=========================================="
echo "User account created successfully!"
echo "=========================================="
echo ""
echo "User Details:"
echo "  Username: $USERNAME"
echo "  Roles: $ROLES"
echo ""
echo "Files modified:"
echo "  - $USERS_FILE"
echo "  - $ROLES_FILE"
echo ""
echo -e "${YELLOW}Note: Restart the Quarkus application for changes to take effect.${NC}"
echo ""

# Option to add inline configuration to application.properties as well
read -p "Also add inline config to application.properties? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Add inline user config
    sed -i "/^# quarkus.security.users.embedded.users.${USERNAME}=.*$/d" "$APP_PROPS"
    sed -i "/^quarkus.security.users.embedded.users.${USERNAME}=.*$/d" "$APP_PROPS"
    echo "quarkus.security.users.embedded.users.${USERNAME}=${PASSWORD}" >> "$APP_PROPS"

    # Add inline roles config
    sed -i "/^# quarkus.security.users.embedded.roles.${USERNAME}=.*$/d" "$APP_PROPS"
    sed -i "/^quarkus.security.users.embedded.roles.${USERNAME}=.*$/d" "$APP_PROPS"
    echo "quarkus.security.users.embedded.roles.${USERNAME}=${ROLES}" >> "$APP_PROPS"

    echo -e "${GREEN}Inline configuration added to $APP_PROPS${NC}"
fi

echo ""
echo "Done."