# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Architecture

The "myth" project is a distributed transaction framework designed to ensure data consistency across microservices using a reliable messaging pattern. It integrates with popular RPC frameworks and message queues to guarantee the eventual execution of transactions.

The core components of the architecture include:

- **`myth-core`**: The heart of the framework, containing the logic for transaction handling, log storage, and annotation processing.
- **RPC Framework Support**: Modules like `myth-dubbo`, `myth-motan`, and `myth-springcloud` provide seamless integration with their respective RPC frameworks.
- **Message Queue Support**: Modules such as `myth-jms`, `myth-kafka`, `myth-rabbitmq`, and `myth-rocketmq` allow the framework to use various messaging systems for reliable message delivery.
- **Transaction Log Storage**: The framework supports multiple backends for storing transaction logs, including Redis, MongoDB, Zookeeper, file, and MySQL. This is configured in `myth-core`.
- **`myth-admin`**: A web-based dashboard for monitoring and managing transaction logs.

## Common Commands

### Build

To build the entire project, run the following command from the root directory:

```bash
mvn -DskipTests clean install -U
```

This command will compile the project, run tests (which are skipped with the `-DskipTests` flag), and install the artifacts into your local Maven repository.

## Module Overview

- `myth-admin`: Transaction log management background.
- `myth-annotation`: Common annotations used throughout the framework.
- `myth-common`: Common utility classes and data structures.
- `myth-core`: The core logic of the framework, including transaction processing and log storage.
- `myth-dashboard`: The front-end for the `myth-admin` management background.
- `myth-dubbo`: Provides support for the Dubbo RPC framework.
- `myth-motan`: Provides support for the Motan RPC framework.
- `myth-springcloud`: Provides support for the Spring Cloud RPC framework.
- `myth-spring-boot-starter`: Provides a Spring Boot starter for easy integration.
- `myth-mq`: Contains modules for various message queue implementations (e.g., `myth-kafka`, `myth-rabbitmq`).
- `myth-rpc`: Contains modules for various RPC framework implementations.
- `myth-demo`: Contains demonstration projects for different use cases.