# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Architecture

This project, `problem-spring-web`, provides libraries to simplify the creation of `application/problem+json` responses in Spring applications. It integrates the `zalando/problem` library with Spring's exception handling mechanisms.

The project is a multi-module Maven project with the following key modules:

*   `problem-spring-common`: Contains common logic shared across different Spring modules.
*   `problem-spring-web`: Provides support for Spring Web MVC.
*   `problem-spring-webflux`: Provides support for Spring WebFlux.
*   `problem-spring-web-autoconfigure`: Provides Spring Boot auto-configuration.
*   `problem-spring-web-starter`: A starter module for easy integration into Spring Boot projects.
*   `problem-violations`: Contains logic for handling constraint violations.

The core design pattern is the use of "advice traits," which are interfaces with default methods that implement `@ExceptionHandler` for specific exceptions. This allows for a compositional approach to exception handling.

## Common Commands

The project uses Maven for its build system. Here are some common commands:

*   **Build the project:**
    ```bash
    ./mvnw clean install
    ```
*   **Run tests:**
    ```bash
    ./mvnw test
    ```
*   **Check for dependency vulnerabilities:**
    ```bash
    ./mvnw dependency-check:check
    ```
