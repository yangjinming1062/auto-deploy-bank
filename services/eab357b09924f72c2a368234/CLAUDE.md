# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- **Run the development server:**
  ```bash
  python dev.py
  ```

- **Run the production server:**
  ```bash
  python app.py
  ```

- **Run database initialisation:**
  ```bash
  python init_mysql.py
  ```

## High-level Code Architecture

This project is a card secret/key sales system built with a Vue.js 3.0 frontend and a Flask backend.

- **Backend:** The main Flask application is in `app.py`. It registers blueprints from:
  - `service/api/user.py`: Handles user-facing endpoints.
  - `service/api/admin.py`: Handles admin-only endpoints.
  - `service/api/common.py`: Handles endpoints shared between users and admins.

  The database is configured in `service/api/db.py` and uses SQLAlchemy. The default database is SQLite, but it can be configured to use MySQL or PostgreSQL.

- **Frontend:** The frontend is built with Vue.js 3.0 and the source code is located in the `public/` directory. The built frontend assets are served from the `dist/` directory.
