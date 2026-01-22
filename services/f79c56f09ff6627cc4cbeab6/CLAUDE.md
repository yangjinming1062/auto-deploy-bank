# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A comprehensive Spring Boot 3.2.5 + Java 17 backend template (v2.2.1-jdk17-pre) integrating multiple middleware and frameworks for enterprise application development.

**Key Technologies:**
- **Web**: Spring Boot Web (Undertow), Sa-Token (Auth), Knife4j (API Docs)
- **Data**: MySQL 8, MyBatis-Plus, ShardingSphere (Sharding), Dynamic Datasource
- **Cache/Queue**: Redis (Lettuce), Redisson (Dist. Lock), Caffeine (Local), RabbitMQ
- **Search**: Elasticsearch 7 (via Easy-ES)
- **AI**: Spring AI 1.0.1 (OpenAI, Ollama, DeepSeek, etc.)
- **Storage**: OSS (MinIO, Tencent COS, Aliyun OSS)

## Build & Run

This is a Maven project using Spring Profiles (`dev` is default).

1.  **Database Setup**:
    - Execute `sql/init_db.sql`, `sql/init_xxl_job.sql`, and `sql/init_power_job.sql` in your MySQL instance.
    - Default admin: `admin` / `123456`
    - Update `src/main/resources/mysql/mysql-dev.yaml` with your DB credentials.

2.  **Build**:
    ```bash
    mvn clean package -Pdev
    ```

3.  **Run**:
    ```bash
    java -jar target/spring-boot-init-template-v2.2.1-jdk17-pre-dev.jar
    ```
    - API Docs: `http://localhost:38080/api/doc.html`

4.  **Test**:
    ```bash
    mvn test
    ```
    - JUnit5 tests are available. Note that `maven.test.skip` is true in `dev` and `prod` profiles, so explicitly run tests if needed.

## Configuration

- **Profiles**: `dev` (default), `prod`. Configure via `src/main/resources/application-{profile}.yaml`.
- **Modular Features**: Most middleware (Redis, MQ, OSS, etc.) are feature-gated. Search for `todo` in `application-xxx.yaml` to enable them.
- **MySQL**: Uses ShardingSphere. Main config is `src/main/resources/mysql/mysql-{profile}.yaml`.

## Architecture

- **Main Package**: `top.sharehome.springbootinittemplate`
- **Modular Design**:
    - `src/main/java/.../config`: Centralized configurations (Web, Cache, MQ, Security, etc.).
    - `src/main/java/.../controller`: REST API endpoints.
    - `src/main/java/.../service`: Business logic.
    - `src/main/java/.../mapper`: MyBatis-Plus mappers (look for `mapper` directory).
    - `src/main/java/.../utils`: Utility classes (Redisson, Caffeine, RabbitMQ, etc.).
    - `src/main/java/.../job`: Scheduled tasks (Standalone Spring, XxlJob, PowerJob).
- **Specialized Packages**:
    - `module/`: Contains external platform modules (xxl-job-admin, power-job-admin, spring-boot-admin, canal-component).
    - `ui/`: Vue.js frontend template (vue-admin-template).