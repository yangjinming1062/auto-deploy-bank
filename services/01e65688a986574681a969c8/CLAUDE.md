# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SHABAN-MD is a WhatsApp bot built with Node.js using the Baileys library for multi-device WhatsApp connectivity. The main source files (`index.js`, `config.js`) are obfuscated using javascript-obfuscator to protect the code.

## Development Commands

```bash
# Install dependencies
npm install

# Start the bot in production (uses pm2)
npm start

# Stop the bot
npm stop

# Restart the bot
npm restart
```

The package.json scripts use pm2 for process management with deep monitoring enabled.

## Architecture

- **index.js**: Main bot entry point (~37,470 lines, obfuscated). Handles WhatsApp connection, message processing, and command routing.
- **config.js**: Configuration file (~40,380 lines, obfuscated). Contains bot settings including Baileys configuration and session management.
- **command.js**: Command registration module (not obfuscated). Defines the `cmd()` function used to register bot commands.

### Command Registration

Commands are registered using the `cmd()` function from `command.js`:

```javascript
cmd({
    name: "commandname",
    desc: "Description",
    category: "category",
    fromMe: false,
    filename: __filename
}, async (client, message, args) => {
    // Command logic
});
```

### Key Dependencies

- `@whiskeysockets/baileys`: WhatsApp multi-device library
- `mongoose`: MongoDB ODM for database operations
- `sequelize`: SQL database ORM (sqlite3, better-sqlite3)
- `express`: Web server framework
- `axios`: HTTP client for API requests
- `pm2`: Process manager for production

## Environment Variables

Key environment variables (set in deployment):
- `SESSION_ID`: WhatsApp session identifier
- `CDN`: CDN URL (defaults to https://bandaheali-cdn.koyeb.app)

## Deployment

The project supports deployment on:
- Heroku (via heroku.yml or app.json)
- Render (via render.yaml)
- Railway
- Traditional VPS with pm2

## Code Structure Notes

The bot uses an event-driven architecture with:
- Baileys socket events for WhatsApp connectivity
- Command pattern for message handling
- Middleware-like filtering for command processing

The obfuscated files cannot be meaningfully modified without first deobfuscating them. If working on bot features, consider:
1. Using the `command.js` patterns for new commands
2. Following the existing command structure and categories
3. The `Shaban/` directory contains SVG assets for the bot's interface