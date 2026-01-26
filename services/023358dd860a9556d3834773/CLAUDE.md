# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Minimal FastAPI "Hello World" application serving as a deployment tutorial template. The application demonstrates basic FastAPI structure and deployment to various cloud platforms (GCP, Heroku, Azure, Ubuntu).

## Commands

### Run Development Server
```bash
uvicorn main:app --reload
```

### Run Production Server (Heroku/PaaS)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Linting
```bash
pylint main.py
```

## Architecture

Single-file FastAPI application (`main.py`). The app exports a `FastAPI` instance named `app` with one endpoint:
- `GET /` - Returns `{"message":"Hello TutLinks.com"}`

The application uses ASGI (uvicorn/gunicorn) and follows standard FastAPI patterns for automatic Swagger documentation at `/docs`.

## Deployment

See README.md for links to deployment tutorials covering:
- Google Cloud Platform (App Engine)
- Heroku
- Azure App Service
- Ubuntu with Caddy 2 web server

Each deployment scenario has corresponding code branches in the upstream repository.