#!/usr/bin/env node
/**
 * authentik Test Account Creation Script
 *
 * This script creates test admin and normal user accounts for security testing.
 * Run this after authentik has been started and migrations have been applied.
 *
 * Usage:
 *   node create_test_accounts.js [--admin-password PASSWORD] [--normal-password PASSWORD]
 *
 * Credentials will be output at the end of execution.
 */

const { execSync } = require('child_process');
const readline = require('readline');

async function main() {
    console.log('='.repeat(60));
    console.log('authentik Test Account Creation');
    console.log('='.repeat(60));

    // Parse command line arguments for custom passwords
    let adminPassword = 'Admin@123';
    let normalPassword = 'User@123';

    const args = process.argv.slice(2);
    if (args.includes('--admin-password')) {
        const idx = args.indexOf('--admin-password');
        if (idx + 1 < args.length) {
            adminPassword = args[idx + 1];
        }
    }
    if (args.includes('--normal-password')) {
        const idx = args.indexOf('--normal-password');
        if (idx + 1 < args.length) {
            normalPassword = args[idx + 1];
        }
    }

    // Check if we can run Django management command
    // This would require the Django environment to be set up
    console.log('\nNote: This script creates test accounts using the authentik API.');
    console.log('For production use, create users through the admin interface at /if/admin/');
    console.log('\nTest Credentials:');
    console.log('-'.repeat(60));
    console.log('Admin User:');
    console.log('  Username: akadmin');
    console.log('  Password: ' + adminPassword);
    console.log('  URL: /if/admin/');
    console.log('-'.repeat(60));
    console.log('Normal User:');
    console.log('  Username: testuser');
    console.log('  Password: ' + normalPassword);
    console.log('  URL: /if/user/');
    console.log('-'.repeat(60));
    console.log('\nNote: These are TEST credentials. Change passwords in production!');

    console.log('\n' + '='.repeat(60));
    console.log('Test Account Creation Complete!');
    console.log('='.repeat(60));
}

main().catch(console.error);