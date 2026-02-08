/**
 * Account Creation Script for Security Testing
 * This script creates test accounts for the pharmacy application
 *
 * Usage: node create-test-accounts.js
 *
 * Accounts created:
 * - Admin user (role: admin)
 * - Normal user (role: user)
 * - Doctor user
 */

const http = require('http');

const BASE_URL = 'http://localhost:3000';

// Helper function to make HTTP requests
function makeRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(body) });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

async function createAccounts() {
  console.log('=== Pharmacy App - Test Account Creation Script ===\n');

  const accounts = [
    {
      type: 'Admin User',
      endpoint: '/api/user/signup',
      data: {
        name: 'Admin User',
        contact: '0771234567',
        nic: '123456789V',
        email: 'admin@test.com',
        password: 'Admin@123',
        role: 'admin'
      }
    },
    {
      type: 'Normal User',
      endpoint: '/api/user/signup',
      data: {
        name: 'Normal User',
        contact: '0779876543',
        nic: '987654321V',
        email: 'user@test.com',
        password: 'User@123',
        role: 'user'
      }
    },
    {
      type: 'Doctor User',
      endpoint: '/api/doctorUser/doctorSignup',
      data: {
        name: 'Dr. Smith',
        contact: '0715555555',
        docId: 'DOC001',
        email: 'doctor@test.com',
        password: 'Doctor@123'
      }
    }
  ];

  const results = [];

  for (const account of accounts) {
    console.log(`Creating ${account.type}...`);
    try {
      const response = await makeRequest('POST', account.endpoint, account.data);

      if (response.status === 201) {
        console.log(`  ✓ ${account.type} created successfully`);
        results.push({
          type: account.type,
          success: true,
          email: account.data.email,
          password: account.data.password
        });
      } else if (response.data.message && response.data.message.includes('duplicate')) {
        console.log(`  ⚠ ${account.type} already exists`);
        results.push({
          type: account.type,
          success: true,
          alreadyExists: true,
          email: account.data.email,
          password: account.data.password
        });
      } else {
        console.log(`  ✗ Failed to create ${account.type}:`, response.data);
        results.push({
          type: account.type,
          success: false,
          error: response.data
        });
      }
    } catch (error) {
      console.log(`  ✗ Error creating ${account.type}:`, error.message);
      results.push({
        type: account.type,
        success: false,
        error: error.message
      });
    }
    console.log('');
  }

  console.log('=== Summary ===');
  console.log(JSON.stringify(results, null, 2));
  console.log('\nTest Credentials:');
  console.log('Admin:   admin@test.com / Admin@123');
  console.log('User:    user@test.com / User@123');
  console.log('Doctor:  doctor@test.com / Doctor@123');
  console.log('\nLogin Endpoints:');
  console.log('  Admin/User: POST /api/user/login');
  console.log('  Doctor:     POST /api/doctorUser/doctorLogin');
}

// Run the script
createAccounts().catch(console.error);