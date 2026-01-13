# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Build:** To build the project and create a WAR file, run:
  ```bash
  ./mvnw clean install
  ```
  or
  ```bash
  mvn clean install
  ```

- **Run:** To run the application, execute the `main` method in `src/main/java/com/fc/V2Application.java`.

- **Test:** To run the tests, you will need to edit the `pom.xml` file and set the `skip` property in the `maven-surefire-plugin` to `false`. Then you can run:
    ```bash
    ./mvnw test
    ```
    or
    ```bash
    mvn test
    ```

## High-Level Architecture

This is a Spring Boot application that provides a web application with a frontend and a backend.

- **Backend:** The backend is a standard Spring Boot application with controllers, services, and repositories. It uses MyBatis for database access and Sa-Token for authentication.
- **Frontend:** The frontend is built with Thymeleaf and is located in the `src/main/resources/templates` directory. Static assets are in `src/main/resources/static`.
- **Configuration:** Application configuration is handled in `src/main/resources/application.yml` and profile-specific files like `application-dev.yml`.

## Database

Before running the application, you need to import the `doc/springbootv2.sql` file into your MySQL database. You will also need to configure the database connection in `src/main/resources/application-dev.yml`.
