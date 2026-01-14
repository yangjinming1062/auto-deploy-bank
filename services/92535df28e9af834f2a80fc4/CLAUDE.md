# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GeoNode is a geospatial content management system built on Django. It provides a platform for managing and publishing geospatial data, combining mature open-source GIS projects under an easy-to-use interface.

## Architecture

GeoNode is a multi-container application with the following key components:

- **Django Application** (`django` service): Main web application handling user requests, data management, and REST API
- **GeoServer** (`geoserver` service): Backend geospatial data server (v2.19.6)
- **Celery Workers** (`celery` service): Async task processing for background jobs
- **Nginx** (`geonode` service): Web server, reverse proxy, and static file serving
- **PostgreSQL + PostGIS** (`db` service): Primary database for geospatial data

The Django application is organized as multiple Django apps within the `geonode/` directory:
- `base/`: Core functionality and base models
- `layers/`: Geospatial layer management
- `maps/`: Map creation and management
- `documents/`: Document management
- `people/`: User profiles and management
- `groups/`: Group management
- `geoserver/`: GeoServer integration
- `api/`: REST API endpoints
- `security/`: Security and permissions
- `services/`: OGC service integration
- `upload/`: Data upload handling
- `monitoring/`: System monitoring
- `social/`: Social features
- `messaging/`: Notifications system

Key configuration files:
- `geonode/settings.py:84369`: Main Django settings (large file - 84KB)
- `docker-compose.yml`: Development/production Docker configuration
- `docker-compose-test.yml`: Test environment configuration
- `requirements.txt`: Python dependencies
- `pyproject.toml`: Build system configuration

## Common Development Commands

### Using Docker Compose

**Start the development environment:**
```bash
docker-compose up -d --build
# Or use Makefile
make auto-up
```

**Build services:**
```bash
docker-compose build django celery
# Or using Makefile
make build
```

**View logs:**
```bash
docker-compose logs -f
# Or using Makefile
make logs
```

**Stop services:**
```bash
docker-compose down
# Or using Makefile
make down
```

### Using Invoke Tasks

The project uses Invoke for task automation (defined in `tasks.py`):

```bash
# Wait for databases to be ready
invoke waitfordbs

# Wait for GeoServer to be ready
invoke waitforgeoserver

# Update environment configuration
invoke update
```

### Database Management

**Run migrations:**
```bash
docker-compose exec django django-admin.py migrate --noinput
# Or using Makefile
make migrate
```

**Load initial data:**
```bash
docker-compose exec django django-admin.py loaddata sample_admin
docker-compose exec django django-admin.py loaddata geonode/base/fixtures/default_oauth_apps_docker.json
docker-compose exec django django-admin.py loaddata geonode/base/fixtures/initial_data.json
# Or using Makefile
make sync
```

**Complete setup (reset database):**
```bash
make reset  # Stops, starts, and syncs the database
make hardreset  # Pulls images, builds, and resets
```

### Django Management Commands

```bash
# Run Django shell
docker-compose exec django python manage.py shell

# Create a superuser
docker-compose exec django python manage.py createsuperuser

# Collect static files
docker-compose exec django python manage.py collectstatic --noinput

# Run a specific management command
docker-compose exec django python manage.py <command>
```

### Static Assets

The frontend uses Grunt for asset compilation (AngularJS, jQuery, Bootstrap):

```bash
cd geonode/static

# Install dependencies (first time)
yarn install

# Watch for changes and rebuild
yarn run watch-less
# or
grunt watch
```

The static assets configuration is in `geonode/static/gruntfile.js` and `geonode/static/package.json`.

## Testing

GeoNode uses pytest for testing with multiple test suites:

### Run Tests

```bash
# Using Makefile
make test  # Runs both smoke and unit tests
make smoketest  # Run only smoke tests
make unittest  # Run only unit tests
```

**Run specific test modules:**
```bash
docker-compose exec django python manage.py test geonode.people.tests --noinput --failfast
docker-compose exec django python manage.py test geonode.base.tests --noinput --failfast
docker-compose exec django python manage.py test geonode.layers.tests --noinput --failfast
docker-compose exec django python manage.py test geonode.maps.tests --noinput --failfast
docker-compose exec django python manage.py test geonode.geoserver.tests --noinput --failfast
```

**Run BDD/Integration tests:**
```bash
docker-compose exec django python -m pytest geonode/tests/bdd/e2e/ --reuse-db
```

**Run specific test file:**
```bash
docker-compose exec django python manage.py test geonode.tests.test_utils --noinput --failfast
```

### Test Directories

- `geonode/tests/smoke.py`: Smoke tests for basic functionality
- `geonode/tests/integration.py`: Integration tests
- `geonode/tests/base.py`: Base test classes
- `geonode/tests/csw.py`: Catalogue Service for the Web tests
- `geonode/tests/utils.py`: Utility test functions
- `geonode/tests/bdd/`: Behavior-driven development tests

### Code Style Checks

**Run flake8:**
```bash
docker-compose exec django flake8 geonode
```

**Run black (code formatting):**
```bash
black geonode
```

**Using pre-commit hooks:**
```bash
pre-commit install  # Install hooks
pre-commit run --all-files  # Run all hooks
```

Configuration:
- `.pre-commit-config.yaml`: Pre-commit hooks configuration (trailing whitespace, end-of-file-fixer, check-yaml, black)
- `pyproject.toml`: Black configuration (120 character line length, excludes migrations and static files)

## Dependencies

### Python Dependencies

Main dependencies are defined in `requirements.txt`:
- **Django 2.2.25**: Web framework
- **Celery 5.2.7**: Async task queue
- **djangorestframework**: REST API framework
- **psycopg2**: PostgreSQL adapter
- **Pillow**: Image processing
- **pyproj, OWSLib, pycsw**: Geospatial libraries
- **Shapely**: Geometric objects manipulation
- **django-haystack + Elasticsearch**: Search functionality

Development dependencies in `requirements_dev.txt`:
- ipdb: Debugger
- pre-commit: Git hooks

Test dependencies in `requirements_tests.txt`:
- pytest, pytest-django: Testing framework
- coverage: Code coverage
- flake8: Linting
- selenium, splinter: Browser testing
- factory-boy: Test data generation

### Frontend Dependencies

Located in `geonode/static/package.json`:
- **AngularJS 1.8.2**: Frontend framework
- **jQuery 3.5.1**: DOM manipulation
- **Bootstrap 3.4.1**: UI components
- **OpenLayers 4.6.5**: Mapping library
- **Grunt**: Build tool

## Development Workflow

### Initial Setup

1. Clone the repository
2. Start services: `make auto-up`
3. Wait for services: `make wait` (or use invoke waitfordbs/waitforgeoserver)
4. Initialize database: `make sync`
5. Access at http://localhost or http://$(DOCKER_HOST_IP)

### Environment Variables

Key environment variables (configured via `tasks.py`):
- `SITEURL`: GeoNode site URL
- `GEOSERVER_LOCATION`: GeoServer instance URL
- `DATABASE_URL`: PostgreSQL connection string
- `GEODATABASE_URL`: PostGIS connection string
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Allowed hostnames

### Making Changes

1. Create a feature branch
2. Make changes to Python code
3. Run tests: `make test`
4. Check code style: `flake8 geonode`
5. Submit pull request

### Contributing Guidelines

From `CONTRIBUTING.md`:
- Add copyright headers to new files (format in CONTRIBUTING.md)
- Include tests for all changes
- Reference GitHub issues in commit messages
- Keep changes focused (one issue per PR)
- Follow existing code style (enforced by flake8 and black)
- Small single-file fixes can be merged by committers
- Large contributions require signing CLA_INDIVIDUAL.md

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b my_bugfix master`
3. Make changes and commit: `git commit -m "fixed bug xyz"`
4. Push branch: `git push origin my_bugfix`
5. Create pull request on GitHub
6. Core developers review and may request changes
7. Be patient - reviews happen in spare time

## Docker Configuration

### Services

- **django**: Main application (port 8000 internal)
- **celery**: Background task worker
- **geonode**: Nginx reverse proxy (ports 80, 443)
- **geoserver**: GeoServer backend (port 8080 internal)
- **db**: PostgreSQL + PostGIS (port 5432 internal)
- **elasticsearch**: Search backend (ports 9200, 9300 internal)
- **redis**: Celery broker (port 6379 internal)

### Volumes

- `statics`: Static and media files
- `geoserver-data-dir`: GeoServer data directory
- `backup-restore`: Backup storage
- `data`: User data storage
- `tmp`: Temporary files

### Health Checks

Services have health checks:
- Django: `curl http://127.0.0.1:8000/`
- GeoServer: `curl http://127.0.0.1:8080/geoserver/rest/workspaces/geonode.html`

## Key Files

- `manage.py`: Django management script
- `pavement.py`: Legacy build automation (Paver)
- `tasks.py`: Invoke-based task automation
- `uwsgi.ini`: uWSGI configuration for Django
- `entrypoint.sh`: Docker entrypoint script
- `geonode/__init__.py:1335`: Version and initialization
- `geonode/version.py:2816`: Version information
- `geonode/urls.py:8791`: URL routing configuration

## Troubleshooting

**Services not starting:**
- Check Docker is running
- Check port conflicts: `docker ps`
- View logs: `make logs`

**Database issues:**
- Reset database: `make reset`
- Check PostgreSQL logs: `docker-compose logs db`

**GeoServer not ready:**
- Wait using: `invoke waitforgeoserver`
- Check GeoServer logs: `docker-compose logs geoserver`

**Static files not loading:**
- Rebuild assets: `cd geonode/static && yarn install && grunt`
- Run `python manage.py collectstatic`

**Tests failing:**
- Run with verbose output: `python manage.py test --verbosity=2`
- Check integration test logs in `geonode/tests/integration.py`
- Use pytest directly for BDD tests: `python -m pytest geonode/tests/bdd/`

## Support

- **Documentation**: https://docs.geonode.org/en/3.x/
- **Demo**: http://master.demo.geonode.org
- **User Mailing List**: https://lists.osgeo.org/cgi-bin/mailman/listinfo/geonode-users
- **Developer Mailing List**: https://lists.osgeo.org/cgi-bin/mailman/listinfo/geonode-devel
- **GitHub Issues**: https://github.com/GeoNode/geonode/issues