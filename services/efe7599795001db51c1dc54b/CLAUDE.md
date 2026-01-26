# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BestBags is a Node.js/Express ecommerce website for selling bags. It uses MongoDB/Mongoose for data storage, EJS for server-side templating, and includes an admin panel built with AdminBro.

## Commands

```bash
# Start the application
npm start

# Start with nodemon for development
npm run dev
```

**Setup required before running:**
1. Create a `.env` file with required environment variables (see README.md)
2. Seed the database:
   ```bash
   cd seedDB && node category-seed.js && node products-seed.js
   ```

## Architecture

### Application Structure (MVC)

- **app.js** - Main entry point; configures Express, middleware, sessions, passport, and routes
- **routes/** - Route handlers for `/`, `/products`, `/user`, `/pages`, and `/admin`
- **models/** - Mongoose schemas (User, Product, Category, Cart, Order)
- **views/** - EJS templates organized by feature (shop/, pages/, user/, partials/)
- **config/** - Database connection, Passport strategy, and validation rules
- **middleware/** - Authentication middleware (`isLoggedIn`, `isNotLoggedIn`)

### Key Patterns

**Authentication:** Passport.js with local strategy (email/password). Routes protected by `middleware.isLoggedIn` and `middleware.isNotLoggedIn`.

**Session/Cart Management:**
- Unauthenticated users: Cart stored in session only
- Authenticated users: Cart persisted to MongoDB via Cart model
- On login: Session cart merges into user's DB cart
- Session config uses MongoStore with 3-hour expiry

**CSRF Protection:** All forms use `csurf` middleware. Routes apply `csrfProtection` and pass `csrfToken` to views.

**Database Denormalization:** Cart items repeat `title`, `price`, `productCode` fields (not just productId) because AdminBro doesn't populate deep nested references.

### External Services

- **Stripe** - Payment processing in checkout route (`routes/index.js`)
- **AdminBro** - Admin panel at `/admin` with custom React components
- **Nodemailer** - Contact form email handling
- **Mapbox** - Map display on about page

## Route Map

| Path | File | Purpose |
|------|------|---------|
| `/` | routes/index.js | Home page, cart operations, checkout |
| `/products` | routes/products.js | Product listing, search, category pages |
| `/products/:slug/:id` | routes/products.js | Product detail |
| `/user/signup` | routes/user.js | User registration |
| `/user/signin` | routes/user.js | User login |
| `/user/profile` | routes/user.js | Order history |
| `/user/logout` | routes/user.js | Sign out |
| `/pages/*` | routes/pages.js | Static pages (about, contact) |
| `/admin/*` | routes/admin.js | Admin panel (AdminBro) |