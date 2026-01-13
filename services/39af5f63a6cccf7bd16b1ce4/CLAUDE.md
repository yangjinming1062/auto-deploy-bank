# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**wechat-admin** is a WeChat management system (微信管理系统) that provides a web interface for managing WeChat contacts, groups, and messages. Built with Flask (backend) and Vue.js (frontend), it integrates with WeChat through WxPy/ItChat libraries and uses Celery for background tasks.

## Tech Stack

- **Backend**: Flask 0.12.1, Flask-SQLAlchemy, Flask-Migrate, Flask-SSE, Celery 4.0.2
- **Frontend**: Vue.js 2.3.4, Element-UI 1.3.6, Vuex, vue-router
- **Database**: MySQL (primary), Redis (cache & broker)
- **WeChat Integration**: WxPy and ItChat (custom forks with signals support)
- **Server**: Gunicorn
- **Documentation**: MkDocs with Material theme

## Common Commands

### Development Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (using cnpm for speed)
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install

# Initialize database
export FLASK_APP=manager.py
flask initdb
```

### Running the Application

**Option 1: Local Development**

```bash
# Terminal 1: Start backend (Flask dev mode)
python app.py

# Terminal 2: Start Celery workers (after login)
celery -A wechat worker -l info -B

# Terminal 3: Start frontend dev server (port 8080)
npm run dev
```

**Option 2: Production (Gunicorn)**

```bash
# Start backend with Gunicorn
gunicorn app:app --bind 0.0.0.0:8100 -w 6 -t 0

# Start Celery workers (after login)
celery -A wechat worker -l info -B

# Build frontend for production
npm run build
```

**Option 3: Docker**

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# First-time initialization
docker-compose run init

# Start web service
docker-compose run --service-ports -d web

# Start Celery (after login)
docker-compose run -d celery
```

### Database Changes

```bash
# After modifying models, create migration
flask db migrate

# Apply migration
flask db upgrade
```

### API Access

- Web Interface: http://localhost:8100
- Frontend Dev: http://localhost:8080 (proxies to backend)
- API: http://localhost:8100/j/

## Architecture

### Backend Structure

- **app.py**: Flask application factory and configuration
- **views/**: Flask blueprints
  - `api.py`: JSON API endpoints (/j/*)
  - `home.py`: Web UI routes
  - `settings.py`: Configuration management
  - `errors.py`, `exceptions.py`: Error handling
- **models/**: SQLAlchemy models
  - `core.py`: User, Group, MP (Official Accounts) models
  - `messaging.py`: Message and notification models
  - `setting.py`: System configuration
  - `redis.py`: Redis utilities
- **wechat/**: Celery tasks and configuration
  - `tasks.py`: Background tasks (contact sync, message handling, listener)
  - `celery.py`: Celery app configuration
  - `celeryconfig.py`: Celery settings
- **libs/**: Core utilities
  - `wx.py`: WxPy/ItChat wrapper and bot management
  - `listener.py`: Message listener implementation
  - `globals.py`: Global state management

### Frontend Structure (src/)

- **main.js**: Vue app entry point
- **App.vue**: Root component
- **routes.js**: Vue Router configuration
- **views/**: Page components (contacts, groups, messages, settings)
- **components/**: Reusable Vue components
- **api/**: API client layer (Axios)
- **vuex/**: State management
- **assets/**: Static assets

### Key Components

1. **User Model** (`models/core.py:47`): Represents WeChat contacts with relationships to friends, groups, and official accounts
2. **Group Model** (`models/core.py:104`): Manages group chats with member relationships
3. **Message Listener** (`libs/listener.py`): Processes incoming WeChat messages via Celery
4. **Plugin System**: Located in PLUGIN_PATHS directory, includes tuling (robot), chatter (chatbot), help (commands)

### Data Flow

1. User logs in via web interface → QR code scan → WxPy/ItChat establishes WeChat connection
2. Celery task `listener()` runs continuously to receive messages
3. `retrieve_data()` task syncs contacts, groups, and official accounts periodically
4. Messages are stored in database and streamed to frontend via SSE (`/stream`)
5. Frontend communicates with backend through API (`/j/*` endpoints)

### Real-time Updates

The application uses Server-Sent Events (SSE) for real-time communication:
- Endpoint: `/stream`
- Used for: Message notifications, login status, system events
- Published via Flask-SSE in `ext.py`

## Configuration

### Local Settings

Create `local_settings.py` to override default configuration from `config.py`:

```python
# Example customizations
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@host/dbname'
REDIS_URL = 'redis://localhost:6379/0'
PLUGINS = ['tuling', 'help']  # Customize plugins
```

### Environment Variables

- `FLASK_APP=manager.py`: Required for Flask CLI commands
- `WERKZEUG_DEBUG_PIN=off`: Disable Werkzeug reloader (if needed)

### Plugin Configuration

Plugins are defined in `config.py`:
- `PLUGIN_PATHS`: List of directories containing plugins
- `PLUGINS`: List of enabled plugin names

Core plugins:
- `tuling`: Tuling robot integration
- `chatter`: ChatterBot integration
- `help`: Command help system

## Important Files

- **app.py:11-25**: Flask app factory with middleware configuration
- **ext.py**: Database and SSE initialization
- **wechat/tasks.py:147-158**: Core Celery tasks (listener, retrieve_data, updates)
- **views/api.py**: REST API endpoints for frontend
- **config.py**: Application configuration and defaults
- **docker-compose.yaml**: Docker service definitions
- **manager.py**: Database initialization command

## Known Issues & Tips

1. **puid not found errors**: Re-login or manually trigger `retrieve_data.delay()`
2. **Gunicorn hanging**: Use `-t 0` for no timeout (required for SSE), or use Flask dev mode
3. **Login requirements**: First login triggers full sync (contacts, groups, members) - takes time
4. **WeChat limitations**: Cannot run simultaneously with official WeChat clients
5. **Environment security**: WeChat web API may block accounts - use dedicated accounts on VPS

## Testing

No explicit test framework configured. For manual testing:
1. Start all services
2. Visit http://localhost:8100
3. Scan QR code with WeChat
4. Wait for contact sync completion
5. Test messaging, group management features

## Documentation

- Project docs: http://localhost:8000 (run `mkdocs serve`)
- Plugin docs: Available at `/docs/plugins.md`

## Development Notes

- Python 3.5+ required
- Node.js 4.0+ for frontend build
- Database migrations via Flask-Migrate
- Avatar images stored in `static/img/avatars/`
- Uploaded files in `uploads/` directory