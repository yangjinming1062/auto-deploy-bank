# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a comprehensive collection of tutorials and demo projects by 程序员欣宸 (Programmer Xinchen) covering:
- **Java ecosystem**: Spring Boot, Quarkus, MyBatis, gRPC, JUnit5, Jackson, Disruptor
- **Go ecosystem**: client-go, Kubernetes clients, gRPC
- **Cloud Native**: Docker, Kubernetes, Spring Cloud, Service Mesh
- **DevOps**: Jenkins, GitLab CI, Maven, Gradle, Ansible
- **Big Data**: Kafka, Flink, Spark, Elasticsearch, HBase
- **Middleware**: Redis, RabbitMQ, ZooKeeper, Dubbo, Neo4j, etc.

The repository contains ~150+ individual demo projects, each self-contained and demonstrating specific technologies or patterns.

## Project Structure

```
/
├── tutorials/              # Advanced tutorials (mix of Go, Java, Python)
├── [technology-name]*/     # Individual demo projects
│   ├── src/main/           # Source code
│   ├── src/test/           # Test code
│   ├── pom.xml or build.gradle or go.mod
│   ├── Dockerfile          # Many projects have Docker support
│   └── docker-compose.yml  # Multi-service demos
├── ansible-*/              # Ansible playbooks
├── README.md               # Detailed article links (Chinese)
└── LICENSE
```

## Build Systems

### Maven Projects (Majority)
- **Build**: `./mvnw clean package` or `mvn clean package`
- **Run**: `java -jar target/app.jar` or `./mvnw spring-boot:run`
- **Docker**: `mvn docker:build` (Spotify docker-maven-plugin)
- **Test**: `./mvnw test` or `mvn test`

### Gradle Projects
- **Build**: `./gradlew build`
- **Run**: `./gradlew bootRun` or `java -jar build/libs/app.jar`
- **Docker**: Some use Jib plugin
- **Test**: `./gradlew test`

### Go Projects
- **Build**: `go build -o binary-name main.go`
- **Run**: `./binary-name` or `go run main.go`
- **Test**: `go test ./...`
- **Dependencies**: `go mod tidy`

### Docker Projects
- **Build image**: `docker build -t image-name .`
- **Run compose**: `docker-compose up -d`
- **Stop**: `docker-compose down`

## Common Patterns

### 1. Spring Boot Applications
Most Spring Boot projects follow standard structure:
- Main class: `@SpringBootApplication`
- REST controllers in `src/main/java/com/bolingcavalry/`
- Configuration in `application.yml` or `application.properties`
- Tests use JUnit5

Example Spring Boot project: `springbootsidecardemo/`
```bash
cd springbootsidecardemo
./mvnw clean package
java -jar target/app.jar
```

### 2. Kubernetes Demos
Many projects include:
- YAML files in `kubernetes/` subdirectory
- Deployment and Service manifests
- Often use `kubectl apply -f`

Example: `k8stomcatdemo/`, `spring-cloud-k8s-*/`

### 3. Multi-Module Projects
Larger projects (like `grpc-tutorials/`, `spring-cloud-tutorials/`) have:
- Multiple Gradle submodules
- Shared proto files or common utilities
- Individual modules for client/server examples

### 4. Docker-Enabled Projects
Many projects include:
- `Dockerfile` for building images
- `docker-compose.yml` for orchestration
- Health check configurations
- Multi-stage builds

## Testing

### Maven Projects
```bash
# Run all tests
./mvnw test

# Run single test class
./mvnw test -Dtest=ClassName

# Run with coverage
./mvnw jacoco:report
```

### Gradle Projects
```bash
./gradlew test
./gradlew test --tests ClassName
```

### Go Projects
```bash
go test ./...
go test -v ./path/to/test
```

## Key Technology Stacks

### Java/Spring Ecosystem
- Spring Boot 2.x (most common)
- Spring Cloud (Eureka, Config, Gateway)
- MyBatis with Druid
- gRPC with protobuf
- JUnit5 testing
- Jackson JSON processing

### Go Ecosystem
- client-go for Kubernetes APIs
- gRPC-Go
- Cobra for CLI
- Viper for configuration
- GORM for database

### Database Technologies
- MySQL (with replication setup demos)
- MongoDB
- Redis (with sentinel)
- Kafka (various versions)
- Elasticsearch
- HBase

### Cloud Platforms
- Kubernetes (various deployment patterns)
- Docker (multi-stage builds, health checks)
- Spring Cloud Kubernetes

## Development Workflow

1. **Navigate to project directory**
   ```bash
   cd path/to/project
   ```

2. **Identify build system** (check for pom.xml, build.gradle, or go.mod)

3. **Build the project**
   - Maven: `./mvnw clean package`
   - Gradle: `./gradlew build`
   - Go: `go build`

4. **Run tests**
   ```bash
   ./mvnw test  # or ./gradlew test or go test ./...
   ```

5. **Run application**
   - Spring Boot: `./mvnw spring-boot:run`
   - Or: `java -jar target/app.jar`

6. **Container support** (if available)
   ```bash
   docker-compose up -d
   ```

## Important Notes

- All documentation and articles are in **Chinese**
- Projects use various Java versions (mostly Java 8)
- Each project is standalone - dependencies aren't shared
- Many demos include infrastructure setup (databases, message queues)
- Some projects require specific environment setup (minikube, external services)
- The `tutorials/` directory contains more advanced, multi-technology examples

## Common Services

- **Eureka**: Service discovery (spring-cloud-tutorials/)
- **RabbitMQ**: Message queue (rabbitmq*/)
- **Kafka**: Event streaming (kafka*/, flink*/)
- **Redis**: Caching (redisdemo/, redis-*-demo/)
- **MySQL**: Database (mysql-master-slave/)
- **Elasticsearch**: Search (elasticsearch-*/)
- **Kubernetes**: Orchestration (k8s*/, kubernetesclient/)

## Quick Start Commands

```bash
# List all projects
ls -d */

# Find Spring Boot projects
find . -name "pom.xml" -path "*/springboot*" | head -5

# Find Go projects
find . -name "go.mod" | head -5

# Find Docker compose files
find . -name "docker-compose.yml" | head -5

# Build all Maven projects (careful - this will take time!)
for dir in */; do [ -f "$dir/pom.xml" ] && cd "$dir" && ./mvnw clean package -q && cd ..; done
```

## Finding Specific Demos

Use these patterns to locate demos:
```bash
# Spring Boot demos
ls -d springboot*/

# Kubernetes demos
ls -d k8s*/

# Kafka demos
ls -d kafka*/

# All tutorial directories
ls tutorials/
```