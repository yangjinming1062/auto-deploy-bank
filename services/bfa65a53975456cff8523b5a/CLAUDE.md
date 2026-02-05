# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server with debug mode
python run.py

# Run tests (configured in .travis.yml)
python setup.py test

# Initialize the database
from flask_website.database import init_db, engine
init_db()

# Update documentation search index
python update-doc-searchindex.py
```

## Architecture

This is the legacy Flask website (flask.pocoo.org). The application uses:

### Application Structure
- **flask_website/__init__.py**: Flask app factory, config loading, blueprint registration, OpenID initialization
- **websiteconfig.py**: Configuration settings (DEBUG, DATABASE_URI, WHOOSH_INDEX, ADMINS)
- **run.py**: Entry point for running the dev server

### Database Layer (flask_website/database.py)
- SQLAlchemy with SQLite backend
- Models: `User`, `Category`, `Snippet`, `Comment`, `OpenIDAssociation`, `OpenIDUserNonce`
- Session lifecycle managed via `@app.teardown_request` hook
- `db_session.remove()` called after each request

### Search (flask_website/search.py)
- Whoosh full-text search engine
- `Indexable` mixin for search-indexed models (Snippet, DocumentationPage)
- Automatic index updates via SQLAlchemy `after_flush` event listener
- Reindex functions: `reindex_snippets()`, `update_documentation_index()`

### Views/Blueprints (flask_website/views/)
- **general.py**: Home, login/logout, profile, search
- **community.py**: Community pages
- **mailinglist.py**: Mailing list archive
- **snippets.py**: Code snippet management
- **extensions.py**: Extensions listing

### Listings (flask_website/listings/)
- **releases.py**: Flask release versions
- **projects.py**: Related projects
- **extensions.py**: Community extensions

### Authentication
- OpenID authentication via `flask-openid`
- `DatabaseOpenIDStore` persists associations/nonces to SQLAlchemy
- Admin users defined in `websiteconfig.ADMINS`
- Decorators: `requires_login`, `requires_admin`

### Content Formatting (flask_website/utils.py)
- CreoleParser dialect for wiki markup
- Pygments syntax highlighting in code blocks (uses `{{{#!lexer}}}` syntax)
- Custom `CodeBlock` element for syntax-highlighted pre blocks

### Templates
- Genshi templating engine (not Jinja2)
- Templates organized by blueprint in `flask_website/templates/`

## Key Patterns

- Models implement `Indexable` interface for search integration
- Search index updates happen automatically on session flush
- Blueprint names correspond to URL route prefixes
- Jinja filters registered in `flask_website/__init__.py`