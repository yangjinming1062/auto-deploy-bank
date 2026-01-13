# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Scout Suite is a multi-cloud security auditing tool written in Python. It uses a provider-based architecture to support different cloud environments (AWS, Azure, GCP, etc.). The core logic fetches configuration data from cloud provider APIs and generates an HTML report highlighting security risks. Each cloud provider has its own module within the `ScoutSuite/` directory.

## Common Commands

- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  pip install -r dev-requirements.txt
  ```

- **Run tests:**
  ```bash
  pytest
  ```

- **Run linters:**
  ```bash
  flake8 .
  ```

- **Run type checker:**
  ```bash
  mypy .
  ```

- **Run the tool:**
  ```bash
  python scout.py <provider> [options]
  ```
  Replace `<provider>` with the cloud provider to audit (e.g., `aws`, `azure`, `gcp`).
