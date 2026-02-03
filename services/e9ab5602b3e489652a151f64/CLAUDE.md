# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RIAS-GREMORY is a multi-device WhatsApp bot built with Node.js and the Baileys library. It provides various features including AI chat, media downloading, group management, games, and more.

## Common Commands

```bash
# Install dependencies
npm install

# Start the bot with pm2 (recommended for production)
npm start

# Alternative start commands
npm run run   # same as start, uses pm2
npm run asta  # same as start

# Stop the bot
npm run stop
```

## Architecture

### Entry Point
- `index.js` - Main entry point that initializes the bot via `lib/amd.js`

### Core Modules
- `lib/amd.js` - Core bot initialization, WhatsApp connection via Baileys, database sync
- `lib/plugins.js` - Command registration system (`smd()`, `cmd()` functions)
- `lib/serialized.js` - Message serialization and utility functions (`smsg()`, `callsg()`)
- `lib/scraper.js` - External API integrations (Pinterest, Telegram upload, mediafire, etc.)
- `lib/index.js` - Central exports of all available functions and utilities
- `lib/schemes.js` - Database schemas for PostgreSQL
- `lib/asta.js` - Main feature implementations (stickers, AI, YouTube, etc.)

### Plugin System
- **Location**: `/plugins` directory
- **Structure**: Each plugin file exports commands using `smd()` or `cmd()` functions
- **Registration**: Commands are auto-loaded and registered globally

### Database
- **MongoDB**: Connection configured via `MONGODB_URI` env var (lib/database/*.js)
- **PostgreSQL**: Connection via `DATABASE_URL` env var (lib/schemes.js)
- **Local Storage**: `lib/assets/store.json` for in-memory message store

### Configuration
- `config.js` - Main configuration file with environment variable fallbacks
- Key settings: `HANDLERS` (prefix), `OWNER_NUMBER`, `SESSION_ID`, `WORKTYPE`, etc.
- Supports `.env` file for environment variables

## Command Definition Pattern

```javascript
// lib/plugins.js exports these registration functions:
smd({
    pattern: 'commandname',      // Main trigger pattern
    alias: ['alias1', 'alias2'], // Optional aliases
    desc: 'Description',          // Help text
    category: 'category',         // Command category
    use: '<example>',            // Usage format
    fromMe: false,               // Owner-only if true
    filename: __filename         // Required
}, async (message, query) => {
    // Command handler
})
```

## Key Utilities Available in Plugins

```javascript
// Message context object provides:
message.reply(text)           // Reply to message
message.send(content)         // Send new message
message.bot                    // Baileys socket connection
message.chat                   // Current chat JID
message.sender                 // Sender JID
message.mentionedJid          // Array of mentioned users

// Common imports from lib:
const { smd, cmd } = require('../lib/plugins')
const { getBuffer, sleep, parsedJid } = require('../lib')
const { Config } = require('../config')
```

## Environment Variables

Key variables (see config.js for full list):
- `SESSION_ID` - WhatsApp session for authentication
- `MONGODB_URI` - MongoDB connection string
- `DATABASE_URL` - PostgreSQL connection string
- `HANDLERS` - Command prefix (default: '.')
- `OWNER_NUMBER` - Bot owner's WhatsApp number
- `WORKTYPE` - 'private' or 'public' mode
- `OPENAI_API_KEY` - For AI features
- `HEROKU_API_KEY` / `HEROKU_APP_NAME` - Heroku deployment

## Session Management

- Sessions stored in `lib/Sessions/` directory
- `creds.json` contains authentication credentials
- QR code scanning for initial connection
- Supports pairing code authentication

## Notes

- Many source files use obfuscation techniques (string encoding with hex arrays)
- Uses `pm2` for process management in production
- Post-install script runs `puppeteer` browser installation
- Supports Heroku, Koyeb, and other PaaS deployments