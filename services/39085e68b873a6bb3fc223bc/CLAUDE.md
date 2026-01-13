# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Confidant is a secret management service that stores secrets in DynamoDB, encrypted at rest. It provides a web interface for managing secrets and service mappings, as well as a client for services to retrieve their secrets.

## Common Commands

The following commands are available in the `Makefile` and are the primary way to build, test, and run the service:

*   `make up`: Starts the Confidant service using `docker-compose`.
*   `make down`: Stops the Confidant service.
*   `make docker_build`: Builds the Confidant docker image.
*   `make test`: Runs all unit, integration, and frontend tests.
*   `make test_unit`: Runs the Python unit tests.
*   `make test_integration`: Runs the integration tests.
*   `make test_frontend`: Runs the frontend tests.
*   `make docs`: Builds the documentation.

## Architecture

Confidant is a Flask-based Python web application. The main application entry point is in `confidant/app.py`. The application's routes are defined in the `confidant/routes/` directory.

### Data Schema

Confidant uses DynamoDB for storage. The data schema is defined in `docs/root/data_schema.md` and consists of the following tables:

*   `credential`: Stores the current revision of a credential.
*   `archive-credential`: Stores archived revisions of credentials.
*   `service`: Stores the current revision of a service.
*   `archive_service`: Stores archived revisions of services.

### At-Rest Encryption

All metadata in Confidant is stored in clear text, but credential pairs in credentials are stored encrypted at-rest. Confidant uses a configured KMS master key to generate data keys. The encrypted data keys are stored in DynamoDB along with the credential.
