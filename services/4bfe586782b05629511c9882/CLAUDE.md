# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

This repository contains multiple independent Maven/Gradle projects. Most commands must be run within the specific project directory.

### Building (Maven)
In a project directory with `pom.xml`:
```bash
mvn package
```

### Running Locally (Maven)
In a project directory with `pom.xml`:
```bash
mvn jetty:run-exploded
```

Or for App Engine Standard specific projects:
```bash
mvn -Plocal clean appengine:devserver
```

### Deploying to Google App Engine
In a project directory with `pom.xml`:
```bash
mvn package appengine:deploy
```

## Code Style
Follow the [Google Java Style Guide](http://google.github.io/styleguide/javaguide.html).

## Project Structure
This is a collection of standalone samples demonstrating various Google Cloud Platform features for Java.

- **bookshelf**: A full featured CRUD app.
    - `bookshelf-standard`: Tutorials for App Engine Standard Environment.
    - `bookshelf/1-cloud-run`: App Engine Flexible/Cloud Run deployment.
- **helloworld-jsp**: Basic Hello World JSP example.
- **background**: Background functions with Cloud Storage/Pub/Sub examples.