# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Development Server:** `npm run dev`
- **Build:** `npm run build`
- **Start:** `npm run start`
- **Lint:** `npm run lint`
- **Lint (fix):** `npm run lint-fix`
- **Prettier (fix):** `npm run prettier-fix`
- **Run Tests:** `python tests/TestRunner.py`

## Code Architecture

This is a Next.js application with a modular architecture. Here are some key points:

- **Next.js:** The core framework for the application. The main pages and routing are handled by Next.js in the `app/` directory.
- **Components:** Reusable UI components are located in the `components/` directory.
- **Configuration:** The `next.config.js` file contains a significant amount of configuration, including environment variables and settings for various services like authentication (OAuth), payments (Stripe), and the AGiXT API. The configuration is built dynamically by merging smaller configuration objects.
- **Middleware:** The `middleware.tsx` file implements a middleware pipeline using a series of hooks. This is primarily used for handling authentication and routing.
- **Authentication:** The application uses a custom authentication system with support for JWT and OAuth2. The relevant middleware and components are in `components/jrg/auth/`.
- **Styling:** The project uses Tailwind CSS for styling, as indicated by `tailwind.config.js` and `postcss.config.js`.
- **Testing:** The tests are located in the `tests/` directory and are a mix of Python scripts and Jupyter notebooks. The main test runner is `tests/TestRunner.py`.
