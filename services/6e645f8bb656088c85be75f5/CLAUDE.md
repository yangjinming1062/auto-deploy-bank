# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Architecture

NetBox is a Django-based application that serves as a network "source of truth." It's used for modeling and documenting network infrastructure.

- **Backend:** Django, using a PostgreSQL database and a Redis cache.
- **Frontend:** The UI is built using standard Django templates with some JavaScript.
- **Data Model:** The core of NetBox is its comprehensive data model, representing network objects like Racks, Devices, IP Addresses, VLANs, and Circuits. The model definitions can be found in the various Django apps within the `netbox/` directory (e.g., `netbox/dcim/models.py`, `netbox/ipam/models.py`).
- **Extensibility:** NetBox supports custom fields, tags, and a plugin system for extending the core functionality. Plugin development documentation is available in the `docs/plugins/` directory.

## Common Development Commands

The following commands are essential for developing in this codebase. Note that `manage.py` commands must be run from the `netbox/` directory.

### Setup

1.  **Install dependencies:**
    ```bash
    python -m pip install -r requirements.txt
    ```
2.  **Configure NetBox:** Copy `netbox/netbox/configuration_example.py` to `netbox/netbox/configuration.py`. For a development environment, set the following:
    - `ALLOWED_HOSTS = ['*']`
    - `DATABASE`: Your PostgreSQL connection details.
    - `REDIS`: Your Redis connection details.
    - `SECRET_KEY`: Generate one using `python netbox/generate_secret_key.py`.
    - `DEBUG = True`
    - `DEVELOPER = True`

### Running the Application

- **Run the development server:**
  ```bash
  cd netbox/ && ./manage.py runserver
  ```

### Running Tests

- **Run the full test suite:**
  ```bash
  export NETBOX_CONFIGURATION=netbox.configuration_testing
  cd netbox/
  python manage.py test
  ```
- **Run tests faster (reuse database):**
  ```bash
  python manage.py test --keepdb
  ```
- **Run a specific test file or test case:**
  ```bash
  python manage.py test dcim.tests.test_views
  ```

### Development Workflow

- **Branching:** Base new work off the `develop` branch for bug fixes and minor features. Use the `feature` branch for major new functionality. The `master` branch tracks the latest stable release.
- **Commits & Pull Requests:** Before submitting a pull request, ensure an issue has been created and assigned to you. Prefix commit messages with `Closes #<issue_number>` to automatically link the PR to the issue.
- **AI-Generated Content:** Per the project's contribution guidelines, any contributions which include AI-generated or reproduced content will be rejected. All work must be original.
