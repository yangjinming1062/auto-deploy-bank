# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level code architecture and structure

This repository contains the source code for LocalStack, a framework for emulating AWS cloud services locally. The core logic is written in Python.

The `localstack/` directory contains the main source code, including the different service implementations. The `tests/` directory contains the integration and unit tests. The project uses `docker` to run the localstack environment.

A key tool for interacting with the local AWS services is `awslocal`, a CLI wrapper that simplifies the process of targeting the local endpoints.

## Common Commands

Here are some common commands used for development in this repository:

*   **`make install`**: Install all dependencies required for development and testing. This sets up a virtual environment and installs all necessary packages.
*   **`make test`**: Run the automated tests. This includes both unit and integration tests.
*   **`make lint`**: Run the code linter to check for code style issues.
*   **`make infra`**: Start the localstack infrastructure directly on the host for development and testing.
*   **`docker-build`**: Build the main Docker image for localstack.
*   **`docker-run`**: Run the localstack Docker image.
*   **`awslocal`**: Use this command-line tool to interact with the local AWS services. For example, `awslocal kinesis list-streams`.
