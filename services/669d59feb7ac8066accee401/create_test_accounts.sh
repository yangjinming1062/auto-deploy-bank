#!/bin/bash
# SiYuan Test Account Creation Script
# This script creates test accounts in the SiYuan configuration file

CONFIG_FILE="$HOME/.siyuan/conf.json"

# Create backup
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    echo "Backup created at $CONFIG_FILE.backup"
fi

# Check if jq is available, otherwise use python for JSON manipulation
if command -v jq &> /dev/null; then
    # Using jq to add accounts to the publish.auth.accounts array
    jq --arg username "admin" --arg password "Admin@123" \
       '.publish.auth.accounts += [{"username": $username, "password": $password, "memo": "Test admin account"}]' \
       "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"

    jq --arg username "normal" --arg password "User@123" \
       '.publish.auth.accounts += [{"username": $username, "password": $password, "memo": "Test normal user account"}]' \
       "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"

    echo "Accounts added using jq"
else
    # Fallback to python
    python3 << 'EOF'
import json
import os

config_file = os.path.expanduser("~/.siyuan/conf.json")

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Ensure publish.auth.accounts exists
    if 'publish' not in config:
        config['publish'] = {}
    if 'auth' not in config['publish']:
        config['publish']['auth'] = {'accounts': []}
    if 'accounts' not in config['publish']['auth']:
        config['publish']['auth']['accounts'] = []

    # Add admin account
    admin_exists = any(acc.get('username') == 'admin' for acc in config['publish']['auth']['accounts'])
    if not admin_exists:
        config['publish']['auth']['accounts'].append({
            'username': 'admin',
            'password': 'Admin@123',
            'memo': 'Test admin account'
        })

    # Add normal user account
    normal_exists = any(acc.get('username') == 'normal' for acc in config['publish']['auth']['accounts'])
    if not normal_exists:
        config['publish']['auth']['accounts'].append({
            'username': 'normal',
            'password': 'User@123',
            'memo': 'Test normal user account'
        })

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print("Accounts added using python")
else:
    print(f"Config file not found: {config_file}")
EOF
fi

echo "Test accounts created:"
echo "  - admin / Admin@123 (admin role)"
echo "  - normal / User@123 (standard role)"
echo ""
echo "To use these accounts, ensure publish service is enabled and Basic Auth is configured."
echo "Access the publish service at port 6806 (default) using HTTP Basic Auth."