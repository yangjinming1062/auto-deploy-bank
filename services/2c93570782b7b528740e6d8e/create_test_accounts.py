#!/usr/bin/env python
"""
create_test_accounts.py - Create test accounts for Skyline

This script creates test user accounts for security testing of the Skyline webapp.
Skyline uses HTTP Basic Authentication configured via settings.py, and also has
a users table in MySQL for tracking which user created resources.

Usage:
    python create_test_accounts.py [--admin-password <password>] [--user-password <password>]
"""

import sys
import os

# Add the skyline directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from sqlalchemy import create_engine, text
import settings


def get_engine():
    """Create a SQLAlchemy engine for the Panorama database."""
    connection_string = (
        'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (
            settings.PANORAMA_DBUSER,
            settings.PANORAMA_DBUSERPASS,
            settings.PANORAMA_DBHOST,
            str(settings.PANORAMA_DBPORT),
            settings.PANORAMA_DATABASE
        )
    )
    return create_engine(connection_string)


def create_or_update_user(engine, username, description, is_admin=False):
    """
    Create or update a user in the users table.

    Args:
        engine: SQLAlchemy engine
        username: The username
        description: User description/role
        is_admin: Whether this is an admin user
    """
    query = text("""
        SELECT id FROM users WHERE user = :username
    """)

    with engine.connect() as conn:
        # Check if user exists
        result = conn.execute(query, {"username": username}).fetchone()

        if result:
            # Update existing user
            update_query = text("""
                UPDATE users
                SET description = :description
                WHERE user = :username
            """)
            conn.execute(update_query, {
                "username": username,
                "description": description
            })
            conn.commit()
            print(f"Updated user: {username}")
        else:
            # Insert new user
            insert_query = text("""
                INSERT INTO users (user, description)
                VALUES (:username, :description)
            """)
            conn.execute(insert_query, {
                "username": username,
                "description": description
            })
            conn.commit()
            print(f"Created user: {username}")


def update_webapp_authSettings(admin_username, admin_password, user_username, user_password):
    """
    Update the settings.py file with new authentication credentials.

    Args:
        admin_username: Admin username
        admin_password: Admin password
        user_username: Normal user username
        user_password: Normal user password
    """
    settings_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'skyline', 'settings.py'
    )

    # Read the current settings file
    with open(settings_path, 'r') as f:
        content = f.read()

    # Update WEBAPP_AUTH_USER
    if 'WEBAPP_AUTH_USER = ' in content:
        content = content.replace(
            'WEBAPP_AUTH_USER = \'admin\'',
            f'WEBAPP_AUTH_USER = \'{admin_username}\''
        )

    # Update WEBAPP_AUTH_USER_PASSWORD (admin password)
    # This is a simple replacement for testing purposes
    # In production, you would want more sophisticated handling
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('WEBAPP_AUTH_USER_PASSWORD = '):
            new_lines.append(f"WEBAPP_AUTH_USER_PASSWORD = '{admin_password}'  # Changed by create_test_accounts.py")
        else:
            new_lines.append(line)
    content = '\n'.join(new_lines)

    # Write back to the settings file
    with open(settings_path, 'w') as f:
        f.write(content)

    print(f"Updated settings.py with new credentials")
    print(f"  Admin user: {admin_username}")
    print(f"  Note: Basic Auth uses single credentials - for testing, use admin credentials")


def main():
    parser = argparse.ArgumentParser(
        description='Create test accounts for Skyline security testing'
    )
    parser.add_argument(
        '--admin-password',
        default='Admin@123',
        help='Password for the admin account (default: Admin@123)'
    )
    parser.add_argument(
        '--user-password',
        default='User@123',
        help='Password for the normal user account (default: User@123)'
    )
    parser.add_argument(
        '--admin-user',
        default='admin',
        help='Username for admin account (default: admin)'
    )
    parser.add_argument(
        '--normal-user',
        default='testuser',
        help='Username for normal user account (default: testuser)'
    )

    args = parser.parse_args()

    print("Creating test accounts for Skyline...")
    print("-" * 50)

    try:
        # Create users in the database
        engine = get_engine()

        # Create admin user in database
        create_or_update_user(
            engine,
            args.admin_user,
            'Administrator account for security testing'
        )

        # Create normal user in database
        create_or_update_user(
            engine,
            args.normal_user,
            'Normal user account for security testing'
        )

        print("-" * 50)
        print("Users created successfully in MySQL database!")

        # Update settings for Basic Auth
        print("-" * 50)
        print("Note: Skyline uses HTTP Basic Authentication configured in settings.py")
        print("The login URL is the webapp root path - any endpoint triggers auth")
        print()
        print("For security testing, use:")
        print(f"  URL: <SKYLINE_URL>/ (or any webapp route)")
        print(f"  Username: {args.admin_user}")
        print(f"  Password: {args.admin_password}")

        # Optionally update settings.py
        update_choice = input(
            "\nUpdate settings.py with these credentials? (yes/no): "
        ).strip().lower()

        if update_choice in ('yes', 'y'):
            update_webapp_authSettings(
                args.admin_user,
                args.admin_password,
                args.normal_user,
                args.user_password
            )
            print("\nSettings updated! Restart Skyline webapp to apply changes.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()