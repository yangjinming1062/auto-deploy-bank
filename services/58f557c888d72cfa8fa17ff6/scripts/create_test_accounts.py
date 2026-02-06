#!/usr/bin/env python3
"""
Create test accounts for Coze Studio (OpenCoze) security testing.

This script creates two accounts:
1. admin: An administrator account with full privileges
2. normal: A regular user account with standard privileges

Password: Uses Argon2id hash format (same as the Go backend)
"""

import argparse
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

import mysql.connector
from argon2 import PasswordHasher
from datetime import datetime

# Database configuration - reads from environment or uses defaults
DB_HOST = os.environ.get('MYSQL_HOST', 'mysql')
DB_PORT = int(os.environ.get('MYSQL_PORT', 3306))
DB_USER = os.environ.get('MYSQL_USER', 'coze')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'coze123')
DB_NAME = os.environ.get('MYSQL_DATABASE', 'opencoze')

def get_db_connection():
    """Get MySQL database connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def hash_password(password: str) -> str:
    """
    Hash password using Argon2id format (matching Go backend).
    Returns hash string compatible with the Go implementation.

    The Go code uses: $argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>
    """
    ph = PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        salt_len=16
    )
    return ph.hash(password)

def verify_password(password: str, hash_str: str) -> bool:
    """Verify password against Argon2id hash."""
    ph = PasswordHasher()
    try:
        return ph.verify(hash_str, password)
    except:
        return False

def create_user(cursor, user_data: dict) -> int:
    """Create a user in the database and return the user ID."""
    insert_query = """
    INSERT INTO `user` (name, unique_name, email, password, description, icon_uri,
                       user_verified, locale, session_key, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    now_ms = int(datetime.now().timestamp() * 1000)

    cursor.execute(insert_query, (
        user_data['name'],
        user_data['unique_name'],
        user_data['email'],
        user_data['password'],
        user_data['description'],
        user_data['icon_uri'],
        user_data['user_verified'],
        user_data['locale'],
        user_data['session_key'],
        now_ms,
        now_ms
    ))
    return cursor.lastrowid

def create_space(cursor, space_data: dict) -> int:
    """Create a space (workspace) in the database and return the space ID."""
    insert_query = """
    INSERT INTO `space` (owner_id, name, description, icon_uri, creator_id, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    now_ms = int(datetime.now().timestamp() * 1000)

    cursor.execute(insert_query, (
        space_data['owner_id'],
        space_data['name'],
        space_data['description'],
        space_data['icon_uri'],
        space_data['creator_id'],
        now_ms,
        now_ms
    ))
    return cursor.lastrowid

def create_space_user(cursor, space_user_data: dict) -> int:
    """Create a space user association in the database."""
    insert_query = """
    INSERT INTO space_user (space_id, user_id, role_type, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    now_ms = int(datetime.now().timestamp() * 1000)

    cursor.execute(insert_query, (
        space_user_data['space_id'],
        space_user_data['user_id'],
        space_user_data['role_type'],
        now_ms,
        now_ms
    ))
    return cursor.lastrowid

def check_user_exists(cursor, email: str) -> bool:
    """Check if a user with the given email already exists."""
    cursor.execute("SELECT id FROM `user` WHERE email = %s", (email,))
    return cursor.fetchone() is not None

def delete_user_by_email(cursor, email: str) -> bool:
    """Delete a user by email (and associated data)."""
    # First get user ID
    cursor.execute("SELECT id FROM `user` WHERE email = %s", (email,))
    result = cursor.fetchone()
    if not result:
        return False

    user_id = result[0]

    # Delete space users
    cursor.execute("DELETE FROM space_user WHERE user_id = %s", (user_id,))
    # Delete spaces where user is owner
    cursor.execute("DELETE FROM `space` WHERE owner_id = %s", (user_id,))
    # Delete user
    cursor.execute("DELETE FROM `user` WHERE id = %s", (user_id,))
    return True

def main():
    parser = argparse.ArgumentParser(description='Create test accounts for Coze Studio')
    parser.add_argument('--admin-email', default='admin@test.com',
                        help='Email for admin account')
    parser.add_argument('--admin-password', default='Admin@123',
                        help='Password for admin account')
    parser.add_argument('--user-email', default='user@test.com',
                        help='Email for normal user account')
    parser.add_argument('--user-password', default='User@123',
                        help='Password for normal user account')
    parser.add_argument('--recreate', action='store_true',
                        help='Delete existing accounts before creating new ones')

    args = parser.parse_args()

    print("=" * 60)
    print("Coze Studio Test Account Creation Script")
    print("=" * 60)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check table exists
        cursor.execute("SHOW TABLES LIKE 'user'")
        if not cursor.fetchone():
            print("ERROR: 'user' table not found. Please run database migrations first.")
            sys.exit(1)

        # Check if tables exist
        cursor.execute("SHOW TABLES LIKE 'space'")
        has_spaces = cursor.fetchone() is not None
        cursor.execute("SHOW TABLES LIKE 'space_user'")
        has_space_users = cursor.fetchone() is not None

        admin_hash = hash_password(args.admin_password)
        user_hash = hash_password(args.user_password)

        admin_data = {
            'name': 'Admin User',
            'unique_name': 'admin',
            'email': args.admin_email,
            'password': admin_hash,
            'description': 'Administrator account for security testing',
            'icon_uri': 'https://example.com/avatars/admin.png',
            'user_verified': True,
            'locale': 'en-US',
            'session_key': 'admin_test_session_key'
        }

        user_data = {
            'name': 'Test User',
            'unique_name': 'testuser',
            'email': args.user_email,
            'password': user_hash,
            'description': 'Normal user account for security testing',
            'icon_uri': 'https://example.com/avatars/user.png',
            'user_verified': True,
            'locale': 'en-US',
            'session_key': 'user_test_session_key'
        }

        # Handle recreation
        if args.recreate:
            print("\n[*] Deleting existing test accounts (if any)...")
            delete_user_by_email(cursor, args.admin_email)
            delete_user_by_email(cursor, args.user_email)
            conn.commit()

        # Check and create admin user
        print("\n[*] Creating admin account...")
        if check_user_exists(cursor, args.admin_email):
            print(f"    - Admin user {args.admin_email} already exists (skipping)")
        else:
            admin_id = create_user(cursor, admin_data)
            print(f"    - Admin user created with ID: {admin_id}")
            print(f"    - Email: {args.admin_email}")
            print(f"    - Password: {args.admin_password}")

            # Create admin's personal space if tables exist
            if has_spaces and has_space_users:
                admin_space = {
                    'owner_id': admin_id,
                    'name': 'Admin Workspace',
                    'description': 'Admin personal workspace',
                    'icon_uri': 'https://example.com/spaces/admin.png',
                    'creator_id': admin_id
                }
                space_id = create_space(cursor, admin_space)
                print(f"    - Admin workspace created with ID: {space_id}")

                # Add admin as owner of the space (role_type=1)
                create_space_user(cursor, {
                    'space_id': space_id,
                    'user_id': admin_id,
                    'role_type': 1  # owner
                })
                print(f"    - Admin added as workspace owner")

        # Check and create normal user
        print("\n[*] Creating normal user account...")
        if check_user_exists(cursor, args.user_email):
            print(f"    - Normal user {args.user_email} already exists (skipping)")
        else:
            user_id = create_user(cursor, user_data)
            print(f"    - Normal user created with ID: {user_id}")
            print(f"    - Email: {args.user_email}")
            print(f"    - Password: {args.user_password}")

            # Create user's personal space if tables exist
            if has_spaces and has_space_users:
                user_space = {
                    'owner_id': user_id,
                    'name': 'User Workspace',
                    'description': 'Normal user personal workspace',
                    'icon_uri': 'https://example.com/spaces/user.png',
                    'creator_id': user_id
                }
                space_id = create_space(cursor, user_space)
                print(f"    - User workspace created with ID: {space_id}")

                # Add user as owner of the space (role_type=1)
                create_space_user(cursor, {
                    'space_id': space_id,
                    'user_id': user_id,
                    'role_type': 1  # owner
                })
                print(f"    - User added as workspace owner")

        conn.commit()
        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("ACCOUNT CREATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nCredentials Summary:")
        print("-" * 40)
        print(f"Admin Account:")
        print(f"  Email: {args.admin_email}")
        print(f"  Password: {args.admin_password}")
        print(f"  Login URL: /passport/web/email/login/")
        print()
        print(f"Normal User Account:")
        print(f"  Email: {args.user_email}")
        print(f"  Password: {args.user_password}")
        print(f"  Login URL: /passport/web/email/login/")
        print("-" * 40)

    except mysql.connector.Error as e:
        print(f"\nERROR: Database error occurred: {e}")
        print("Please ensure MySQL is running and credentials are correct.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()