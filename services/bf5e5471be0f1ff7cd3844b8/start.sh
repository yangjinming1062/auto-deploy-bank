#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."

MYSQL_HOST="${MYSQL_HOST:-mysql}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_USER="${MYSQL_USER:-root}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-rootpassword}"

max_attempts=180
attempt=0

while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts: Checking MySQL connection..."

    if mysqladmin ping -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" --ssl=0 --silent 2>/dev/null; then
        echo "MySQL is ready!"
        break
    fi

    if [ $attempt -eq $max_attempts ]; then
        echo "Failed to connect to MySQL after $max_attempts attempts"
        exit 1
    fi

    echo "MySQL not ready yet, waiting 2 seconds..."
    sleep 2
done

echo "Starting chatdb.py..."
if [ "${WEB_MODE:-false}" = "true" ]; then
    exec python webapp.py
else
    exec python chatdb.py
fi