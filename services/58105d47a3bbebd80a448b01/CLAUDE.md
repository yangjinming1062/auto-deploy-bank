# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- **Build the project:**
  ```bash
  mvn clean package -DskipTests
  ```

- **Run tests:**
  ```bash
  mvn test
  ```

- **Run a single test:**
  ```bash
a  mvn -Dtest=ClassName#methodName test
  ```

## High-level Code Architecture

PowerJob is a distributed job scheduling framework with a server-worker architecture.

- **`powerjob-server`**: The core of the application, responsible for task management and scheduling. It persists job information in a database and distributes tasks to `powerjob-worker` instances.

- **`powerjob-worker`**: The execution side of the application, responsible for running tasks. It receives tasks from the `powerjob-server` and executes them.

- **`powerjob-client`**: Provides a simple API for developers to interact with the `powerjob-server`.

- **`powerjob-common`**: Contains common data structures and utility classes used by other modules.

- **`powerjob-remote`**: Manages communication between the `powerjob-server`, `powerjob-worker`, and `powerjob-client` using Akka.
