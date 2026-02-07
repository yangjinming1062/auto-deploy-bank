#!/bin/bash
# Script to create admin accounts for the MyBlog Spring Boot application
# Usage: ./create_admin_account.sh [admin|normal] [username] [password]

ROLE=${1:-admin}
USERNAME=${2:-testadmin}
PASSWORD=${3:-Test@123}

# Check if MySQL client is available
if ! command -v mysql &> /dev/null; then
    echo "MySQL client not found. Please install mysql-client first."
    exit 1
fi

# Database connection settings (can be overridden via environment variables)
DB_HOST=${SPRING_DATASOURCE_HOST:-43.153.15.174}
DB_PORT=${SPRING_DATASOURCE_PORT:-3306}
DB_USER=${SPRING_DATASOURCE_USERNAME:-root}
DB_PASS=${SPRING_DATASOURCE_PASSWORD:-6on5&as.O/#U}
DB_NAME=${SPRING_DATASOURCE_DATABASE:-myblog}

echo "Creating $ROLE account: $USERNAME"
echo "Note: Password will be stored as MD5 hash"

# Check if username already exists
EXISTS=$(mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -N -e "SELECT COUNT(*) FROM admin WHERE adminname='$USERNAME';" 2>/dev/null)

if [ "$EXISTS" -gt 0 ]; then
    echo "User '$USERNAME' already exists. Updating password..."
    # MD5 hash the password
    MD5_PASS=$(echo -n "$PASSWORD" | md5sum | awk '{print $1}')
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "UPDATE admin SET adminpasswd='$MD5_PASS' WHERE adminname='$USERNAME';" 2>/dev/null
    echo "Password updated successfully."
else
    echo "Inserting new user..."
    # MD5 hash the password
    MD5_PASS=$(echo -n "$PASSWORD" | md5sum | awk '{print $1}')
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "INSERT INTO admin (adminname, adminpasswd) VALUES ('$USERNAME', '$MD5_PASS');" 2>/dev/null
    echo "Account created successfully."
fi

echo ""
echo "Account credentials:"
echo "  Username: $USERNAME"
echo "  Password: $PASSWORD"
echo "  Role: $ROLE"
echo ""
echo "Login URL: /login"