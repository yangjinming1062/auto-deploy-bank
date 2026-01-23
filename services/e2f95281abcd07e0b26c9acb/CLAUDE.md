# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DHorse is a cloud application management platform that simplifies Kubernetes deployments without requiring K8s knowledge. It's a multi-module Maven project using Java 8, Spring Boot 2.7.17, and MyBatis-Plus.

## Build Commands

```bash
# Build entire project (skip tests, no test framework configured)
mvn clean package -DskipTests

# Build specific module
mvn -pl dhorse-rest clean package

# Production build (creates tar.gz distribution)
mvn clean package -P release -DskipTests
```

Output: `dhorse-rest-{version}.jar` (fat JAR) and `dhorse-v{version}-bin.tar.gz` distribution archive.

## Run Commands

```bash
# Extract distribution and start
tar zxvf dhorse-rest/target/dhorse-v*-bin.tar.gz
cd dhorse-v*/
bin/dhorse-start.sh

# Service runs on port 8100, default login: admin/admin
# Access at: http://127.0.0.1:8100

bin/dhorse-stop.sh
```

## Architecture

### Module Dependencies (Bottom-Up)
```
dhorse-rest → dhorse-application → dhorse-infrastructure → dhorse-api
dhorse-agent (standalone Java agent, loads JVM metrics)
```

### Layered Architecture
- **dhorse-api**: DTOs, enums, events, base response/param classes
- **dhorse-infrastructure**: MyBatis repositories, persistence strategies, utilities
- **dhorse-application**: Business services (ApplicationService pattern)
- **dhorse-rest**: Controllers, WebSocket handlers, bootstrap

### Strategy Pattern (Key Extensibility Mechanism)
Infrastructure uses strategies for pluggable behavior:
- **ClusterStrategy**: K8s cluster operations (K8sClusterHelper for deployments, services, configs)
- **LoginStrategy**: User authentication (Normal, LDAP, CAS, DingTalk, Feishu, WeChat)
- **CodeRepoStrategy**: Source code access (GitLab, GitHub, Codeup)
- **ImageRepoStrategy**: Image registry operations (Harbor, AliCloud)

### Domain Concepts
- **Cluster**: Kubernetes cluster with namespace support
- **AppEnv**: Application deployment target (cluster + namespace + tech stack)
- **AppBranch**: Code branch/tag with build configuration
- **DeploymentVersion**: Deployed version with status tracking
- **DeploymentDetail**: Runtime instances in K8s

### Key Entry Points
- Bootstrap: `org.dhorse.rest.DHorseBootstrap` (port 8100)
- Java Agent: `org.dhorse.agent.JvmMetricsAgent` (for JVM metrics collection)

## Code Conventions

- REST controllers in `dhorse-rest/src/main/java/org/dhorse/rest/resource/`
- Application services in `dhorse-application/src/main/java/org/dhorse/application/service/`
- Repositories extend `BaseRepository` for generic CRUD via MyBatis-Plus
- WebSocket handlers for real-time logs and terminal in `rest/websocket/`

## Configuration

- Main config: `dhorse-rest/src/main/resources/dhorse.yml`
- Private config (not in git): `application-private.yml`
- Environment variables override config values
- Data/log paths configurable; defaults to `/tmp/log`

## Key Technologies

- **ORM**: MyBatis-Plus 3.5.4
- **Kubernetes**: fabric8-client 6.13.4, kubernetes-client 18.0.0
- **Container**: Jib-Core 0.25.0 (Docker image building without Docker daemon)
- **Git**: GitLab4J API 5.0.1
- **Scheduling**: Quartz (auto-deployment jobs)
- **Frontend**: Layui 2.6.3 + jQuery 3.4.1 (served from `static/` directory)
- **Database**: MySQL or SQLite (configurable via dhorse.yml)

## Conventions

- REST response format: `RestResponse<T>` wrapper
- Query parameters: `QueryHelper` for pagination
- No test framework configured; avoid adding tests until JUnit/TestNG is set up

## WebSocket Endpoints

- Build logs: `BuildVersionLogWebSocket`
- Deployment logs: `DeploymentDetailLogWebSocket`
- Replica logs: `ReplicaLogWebSocket`
- Terminal: `TerminalWebSocketHandler` (SSH access to containers)