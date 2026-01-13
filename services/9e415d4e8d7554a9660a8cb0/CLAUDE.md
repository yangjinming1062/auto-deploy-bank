# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Architecture

Flask-AppBuilder is a rapid application development framework built on top of Flask. Its main components are:

- **Database**: Uses SQLAlchemy and supports multiple databases (sqlite, MySQL, ORACLE, etc.). It has partial support for MongoDB. The core models and database logic are within the `flask_appbuilder/` directory.
- **Security**: Provides automatic role-based permissions, various authentication methods (OAuth, OpenID, LDAP, etc.), and self-user registration.
- **Views and Widgets**: Automatically generates menus, CRUD interfaces, and various view widgets like lists and charts.
- **REST API**: Automatically generates CRUD RESTful APIs for models.
- **Forms**: Automatically generates Add, Edit, and Show forms from database models with validation.
- **Internationalization (i18n)**: Supports multiple languages through Babel.

The main application logic is located in the `flask_appbuilder/` directory. Tests are in `tests/`, and examples can be found in the `examples/` directory.

## Common Commands

### Development Environment Setup

To set up a local development environment, run the following commands:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt -r requirements/dev.txt -r requirements/extra.txt
```

You will also need `docker` and `docker-compose` installed.

### Running Tests

To run the test suite against Postgres:

1.  Start the Postgres container:
    ```bash
    docker-compose up -d
    ```

2.  Run the tests:
    ```bash
    nose2 -c setup.cfg -A '!mongo' tests
    ```

Alternatively, you can use `tox`:

```bash
tox -e postgres
```

### Running a Single Test

To run a specific test against a clean Postgres instance:

1.  Reset the database:
    ```bash
    docker-compose down -v
    docker-compose up -d
    ```

2.  Export the database connection string:
    ```bash
    export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://pguser:pguserpassword@0.0.0.0/app
    ```

3.  Execute the test:
    ```bash
    nose2 -v tests.test_api.APITestCase.test_get_item_dotted_mo_notation
    ```

### Code Formatting

To format the code, use `black` and `flake8`:

```bash
black flask_appbuilder tests
flake8 flask_appbuilder tests
```
