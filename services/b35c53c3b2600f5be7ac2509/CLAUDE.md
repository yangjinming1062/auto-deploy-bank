# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains Jpom, a tool for online builds, automated deployment, and project monitoring. The project is a Java-based Maven project with a modular architecture and two separate front-end applications.

### High-Level Architecture

*   **Backend**: The backend is a multi-module Spring Boot application managed by Maven. The core modules are:
    *   `modules/server`: The main Jpom server application.
    *   `modules/agent`: The Jpom agent that runs on managed machines.
    *   `modules/common`: Shared code and utilities used by other modules.
*   **Frontend**: There are two distinct Vue.js front-end applications:
    *   `web-vue`: A modern Vue.js application built with Vite. This is likely the main and most current UI.
    *   `web-vue2`: A legacy Vue 2 application built with Vue CLI.

## Common Commands

### Full Production Build

To build the entire project, including the front-end and back-end applications, run the following commands from the root directory:

```bash
# 1. Build the Vue.js frontend
(cd web-vue && npm install && npm run build)

# 2. Build the Java backend using Maven
mvn clean package
```

This process is also available in the `script/release.sh` script.

### Development

For development, you can run the backend and frontend services separately.

*   **Backend**:
    *   Run the server application by executing the `main` method in `org.dromara.jpom.JpomServerApplication`.
    *   Run the agent application by executing the `main` method in `org.dromara.jpom.JpomAgentApplication`.
*   **Frontend (`web-vue`)**:
    ```bash
    cd web-vue
    npm install
    npm run serve
    ```

### Docker

To build the official Docker image for the server, you can use the script provided:

```bash
# Build and push a multi-platform Docker image
./script/docker.sh
```