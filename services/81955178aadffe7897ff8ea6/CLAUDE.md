# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About the Project

WebGoat is a deliberately insecure web application maintained by OWASP designed to teach web application security lessons. It is a Spring Boot application built with Maven.

## Common Commands

*   **Build the project:**
    ```bash
    ./mvnw clean install
    ```
*   **Run the project:**
    ```bash
    ./mvnw spring-boot:run
    ```
    WebGoat will be available at http://localhost:8080/WebGoat.

*   **Run with Docker:**
    ```bash
    docker run -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:9090:9090 webgoat/webgoat
    ```

## Code Architecture

The main application code is located in `src/main/java/org/owasp/webgoat/`. The project is divided into the following main packages:

*   `container`: Contains the core framework and services for running the lessons.
*   `lessons`: Contains the source code for the individual security lessons. Each lesson is a self-contained module.
*   `server`: Contains the main entry point for the WebGoat application.
*   `webwolf`: A separate application packaged with WebGoat, used for certain lessons that require a target to attack.
