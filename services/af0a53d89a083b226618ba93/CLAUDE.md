# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

*   **Build the project:** `mvn clean install`
*   **Run unit tests:** `mvn test`
*   **Run integration tests:** `mvn verify -Pintegration-tests`
*   **Run API tests:** `mvn verify -Papi-tests`
*   **Run all tests:** `mvn verify -Papi-tests,integration-tests`
*   **Start the application:** `docker compose up -d`
*   **Stop the application:** `docker compose down`

## High-Level Code Architecture

The openrouteservice is a multi-module Maven project written in Java. The main modules are:

*   **ors-engine:** The core routing engine, which is a fork of GraphHopper.
*   **ors-api:** The Spring Boot application that exposes the openrouteservice API.
*   **ors-report-aggregation:** Aggregates test reports.
*   **ors-test-scenarios:** Contains test scenarios.
*   **ors-benchmark:** Contains benchmark tests.

The application is designed to be run in a Docker container. The `Dockerfile` and `docker-compose.yml` files in the root directory are used to build and run the application.

## Development Workflow

1.  Before starting work, create a new issue or choose an existing one.
2.  Create a new branch from `main` with a name that follows the pattern `<[hotfix/bugfix/feat/algo]>/<issue#>-<purpose>`.
3.  Write code and add unit or API tests for new functionality.
4.  Commit your changes with a meaningful message.
5.  Keep the number of commits to a minimum by using `git commit --amend`.
6.  If your branch needs to be updated from `main`, use `git rebase main`.
7.  Push your changes and create a pull request.
