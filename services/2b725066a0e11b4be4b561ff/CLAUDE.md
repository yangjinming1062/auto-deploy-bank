# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is "Whoogle Search," a self-hosted, ad-free, privacy-respecting metasearch engine that gets Google search results without any ads, JavaScript, AMP links, cookies, or IP address tracking. It is a Python-based web application using the Flask framework.

## Common Commands

### Development

**1. Install Dependencies:**

To set up the local development environment, create a virtual environment and install the required packages from `requirements.txt`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Run the Application:**

To run the application locally, use the `run` script:

```bash
./run
```

The application will be available at `http://127.0.0.1:5000` by default.

**3. Run Tests:**

The project uses `pytest` for testing. To run the test suite, use the following command:

```bash
pytest
```

### Docker

**1. Build and Run with Docker:**

You can build and run the application using Docker:

```bash
docker build --tag whoogle-search:1.0 .
docker run --publish 5000:5000 --detach --name whoogle-search whoogle-search:1.0
```

**2. Run with Docker Compose:**

Alternatively, you can use `docker-compose`:

```bash
docker-compose up
```

## High-Level Code Architecture

The application is structured as a standard Flask project:

-   `app/`: Contains the core application logic.
    -   `routes.py`: The main entry point of the application, containing all API routes.
    -   `request.py`: Handles all outbound requests, including proxied and Tor connectivity.
    -   `filter.py`: Contains functions and utilities for filtering content from upstream Google search results.
    -   `static/`: Contains static assets like CSS, JavaScript, and images.
    -   `templates/`: Contains the HTML templates for the application.
-   `test/`: Contains the test suite for the application.
-   `Dockerfile` and `docker-compose.yml`: Define the Docker build and service configurations.
-   `requirements.txt`: Lists the Python dependencies for the project.
-   `setup.cfg`: Contains project metadata and configuration for setuptools.
