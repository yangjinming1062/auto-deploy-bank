# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Setup

1.  **Install system dependencies:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install python-is-python3 xvfb libfontconfig wkhtmltopdf python3-dev python3-pip build-essential libssl-dev libffi-dev python3-venv redis-server redis-tools virtualenv -y
    ```

2.  **Create a virtual environment:**
    ```bash
    virtualenv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file and add the necessary environment variables. Refer to `ENV.md` for the required variables.

### Running the Application

1.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

2.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://localhost:8000`.

3.  **Start the Celery worker:**
    ```bash
    celery -A crm worker --loglevel=INFO
    ```

### Running Tests

To run the test suite, use `pytest`:

```bash
pytest
```

## High-Level Code Architecture

This is a Django-based CRM application. The project is structured into several Django apps, each representing a core feature of the CRM:

*   `accounts/`: User accounts and authentication.
*   `contacts/`: Managing contacts.
*   `leads/`: Lead management.
*   `opportunity/`: Sales opportunities.
*   `cases/`: Customer service cases.
*   `invoices/`: Billing and invoices.
*   `planner/`: Task and event scheduling.
*   `common/`: Shared utilities and functionality.
*   `crm/`: The main project directory containing settings and root URL configuration.

The frontend is not part of this repository. This project provides a REST API, and the frontend is expected to be a separate application (e.g., a React or SvelteKit app). The API endpoints can be explored via the Swagger UI at `http://localhost:8000/swagger-ui/`.

**Note:** This repository is no longer actively maintained. The new version is being developed in a SvelteKit-based repository.
