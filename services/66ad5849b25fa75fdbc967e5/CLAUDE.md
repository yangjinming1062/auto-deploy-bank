# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This directory (`66ad5849b25fa75fdbc967e5`) is a persistent data deployment for the Testsigma application. It does not contain the Testsigma source code. The core application code should be located in a separate repository or directory outside of `deploy/`.

## Infrastructure

- **Database**: MySQL
- **Data Directory**: `./deploy/docker/db_data`
- **Database Name**: `testsigma_opensource`

## Commands

### Accessing the Database

If you need to interact with the MySQL database:

```bash
# Start the database container (if using Docker Compose elsewhere)
docker-compose up -d mysql

# Connect to the MySQL instance
mysql -h 127.0.0.1 -P 3306 -u root -p
# Default password is often 'password' or configured in the main project .env
```

### Managing Docker Data

The `./deploy/docker/db_data` directory contains the persisted MySQL data.

```bash
# Backup the database
tar -czvf mysql_backup.tar.gz ./deploy/docker/db_data

# Restore the database
# Stop the container, replace the db_data directory contents, and restart.
```

## Notes

- If you need to build or run Testsigma, please refer to the main Testsigma repository.
- This directory is likely mounted as a volume in the main application's Docker environment.