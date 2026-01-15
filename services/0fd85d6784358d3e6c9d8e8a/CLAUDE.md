# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Damn Vulnerable Bank is an **intentionally vulnerable Android banking application** designed for security testing and practicing Android application security assessment (OWASP Mobile Top 10). It includes both a Node.js/Express backend API and a native Android app with various security vulnerabilities intentionally included for learning purposes.

## Common Commands

### Backend Server (Node.js/Express)

```bash
# Install dependencies
cd BackendServer && npm install

# Run locally (requires MySQL running)
npm start

# Run with Docker (includes MySQL)
cd BackendServer && docker-compose up -d

# View logs
docker-compose logs -f
```

### Android App

```bash
cd DamnVulnerableBank

# Build debug APK
./gradlew assembleDebug

# Build release APK (unsigned)
./gradlew assembleRelease

# Build release APK with signing (obfuscated)
# Use Android Studio: Build > Generate Signed Bundled/APK > APK > Release

# Run lint checks
./gradlew lint

# Clean build
./gradlew clean
```

## Architecture

### Backend (BackendServer/)

```
BackendServer/
├── bin/www           # Server entry point, creates HTTP server on port 3000
├── app.js            # Express app setup, routes all /api requests
├── config/config.json # Sequelize MySQL configuration (host: mysql for docker)
├── database/         # MySQL schema + seed data (schema+data.sql)
├── middlewares/
│   ├── crypt.js      # XOR-based encryption/decryption (hardcoded SECRET = 'amazing')
│   └── validateToken.js # JWT validation for user and admin tokens
├── models/           # Sequelize models (users, transactions, beneficiaries)
├── routes/index.js   # Main router, combines /api routes
└── lib/api/          # API endpoints organized by resource
    ├── Health/       # Health check endpoint
    ├── User/         # Login, register, profile, change-password
    ├── Balance/      # Account balance operations
    ├── Transactions/ # Transaction history
    └── Beneficiary/  # Beneficiary management
```

**Authentication**: JWT tokens signed with hardcoded secret `"secret"`. Tokens include `username` and `is_admin` claims.

**Encryption**: Custom XOR-based encryption using hardcoded key `'amazing'`. Requests/responses use `enc_data` field with base64-encoded encrypted JSON.

### Android App (DamnVulnerableBank/)

```
DamnVulnerableBank/app/src/main/
├── AndroidManifest.xml    # Exported activities, deep links, permissions
├── java/com/app/damnvulnerablebank/
│   ├── MainActivity.java          # Entry point, configures backend URL
│   ├── BankLogin.java             # Login activity
│   ├── RegisterBank.java          # User registration
│   ├── ViewBalance.java           # View account balance
│   ├── SendMoney.java             # Transfer funds
│   ├── ViewBeneficiary.java       # Manage beneficiaries
│   ├── GetTransactions.java       # Transaction history
│   ├── FridaCheckJNI.java         # Native anti-debugging (via Makefile)
│   ├── RootUtil.java              # Root detection
│   ├── EncryptDecrypt.java        # Client-side encryption wrapper
│   └── ... (other activities)
└── jni/                    # Native code for anti-debugging
```

**Security Features (Intentionally Vulnerable)**:
- Root/emulator detection
- Anti-debugging checks via JNI
- Hardcoded sensitive strings
- SSL pinning (incomplete - documented as to-do)
- WebView integration
- Deep links

### Database Schema

Tables: `users`, `transactions`, `beneficiaries`. Pre-populated with test users:

| username | password | account_number | is_admin |
|----------|----------|----------------|----------|
| user1 | password1 | 111111 | false |
| user2 | password2 | 222222 | false |
| user3 | password3 | 333333 | false |
| user4 | password4 | 444444 | false |
| admin | admin | 999999 | true |

## API Endpoints

All endpoints prefixed with `/api` and require encrypted `enc_data` body (base64, XOR encrypted JSON).

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health/check` | POST | No | Health check |
| `/api/user/login` | POST | No | User login |
| `/api/user/register` | POST | No | User registration |
| `/api/user/profile` | POST | JWT | Get user profile |
| `/api/user/change-password` | POST | JWT | Change password |
| `/api/balance` | POST | JWT | Get account balance |
| `/api/transactions/view` | POST | JWT | View transactions |
| `/api/transactions/add` | POST | JWT | Create transaction |
| `/api/beneficiary/view` | POST | JWT | View beneficiaries |
| `/api/beneficiary/add` | POST | JWT | Add beneficiary |
| `/api/beneficiary/approve` | POST | Admin JWT | Approve beneficiary |

## Key Vulnerabilities for Security Testing

See `/exploits/` guide documentation for detailed walkthroughs:
1. REST API vulnerabilities
2. Sensitive information disclosure
3. Exported activities security
4. WebView via deeplink exploitation

## Documentation

- Full guide: https://rewanthtammana.com/damn-vulnerable-bank/
- MkDocs documentation in `/guide/` directory
- Postman collection: `BackendServer/dvba.postman_collection.json`