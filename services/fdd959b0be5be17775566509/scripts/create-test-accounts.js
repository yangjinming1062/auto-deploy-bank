#!/usr/bin/env node
/**
 * EverShop Test Account Creation Script
 * Creates admin and customer accounts for security testing
 *
 * Usage: node scripts/create-test-accounts.js
 *
 * This script creates:
 * - Admin account: admin@evershop.com / Admin@123
 * - Customer account: customer@evershop.com / User@123
 */

import 'dotenv/config';
import { insertOnUpdate } from '@evershop/postgres-query-builder';
import { pool } from '../packages/evershop/src/lib/postgres/connection.js';
import { hashPassword } from '../packages/evershop/src/lib/util/passwordHelper.js';

const ADMIN_EMAIL = 'admin@evershop.com';
const ADMIN_PASSWORD = 'Admin@123';
const ADMIN_FULLNAME = 'Admin User';

const CUSTOMER_EMAIL = 'customer@evershop.com';
const CUSTOMER_PASSWORD = 'User@123';
const CUSTOMER_FULLNAME = 'Test Customer';

async function createAdminAccount() {
  console.log('Creating admin account...');
  try {
    await insertOnUpdate('admin_user', ['email'])
      .given({
        full_name: ADMIN_FULLNAME,
        email: ADMIN_EMAIL,
        password: hashPassword(ADMIN_PASSWORD)
      })
      .execute(pool);
    console.log(`✓ Admin account created: ${ADMIN_EMAIL} / ${ADMIN_PASSWORD}`);
    return true;
  } catch (e) {
    console.error(`✗ Failed to create admin account: ${e.message}`);
    return false;
  }
}

async function createCustomerAccount() {
  console.log('Creating customer account...');
  try {
    // Check if customer already exists
    const existing = await pool.query(
      'SELECT * FROM customer WHERE email = $1',
      [CUSTOMER_EMAIL]
    );

    if (existing.rows.length > 0) {
      // Update existing customer password
      await pool.query(
        'UPDATE customer SET password = $1, full_name = $2 WHERE email = $3',
        [hashPassword(CUSTOMER_PASSWORD), CUSTOMER_FULLNAME, CUSTOMER_EMAIL]
      );
      console.log(`✓ Customer account updated: ${CUSTOMER_EMAIL} / ${CUSTOMER_PASSWORD}`);
    } else {
      // Insert new customer
      await pool.query(
        `INSERT INTO customer (email, full_name, password, group_id, status)
         VALUES ($1, $2, $3, 1, 1)`,
        [CUSTOMER_EMAIL, CUSTOMER_FULLNAME, hashPassword(CUSTOMER_PASSWORD)]
      );
      console.log(`✓ Customer account created: ${CUSTOMER_EMAIL} / ${CUSTOMER_PASSWORD}`);
    }
    return true;
  } catch (e) {
    console.error(`✗ Failed to create customer account: ${e.message}`);
    return false;
  }
}

async function main() {
  console.log('EverShop Test Account Creation');
  console.log('==============================\n');

  try {
    // Test database connection
    await pool.query('SELECT 1');
    console.log('✓ Database connected\n');
  } catch (e) {
    console.error(`✗ Database connection failed: ${e.message}`);
    console.log('\nMake sure PostgreSQL is running and the .env file is configured correctly.');
    process.exit(1);
  }

  const adminResult = await createAdminAccount();
  const customerResult = await createCustomerAccount();

  console.log('\n==============================');
  if (adminResult && customerResult) {
    console.log('All accounts created successfully!');
    console.log('\nAdmin Login URL: /user/login');
    console.log('Customer Login URL: /customer/login');
  } else {
    console.log('Some accounts failed to create. Check errors above.');
    process.exit(1);
  }

  await pool.end();
}

main();