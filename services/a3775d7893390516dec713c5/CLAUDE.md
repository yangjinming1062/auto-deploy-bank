# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SkyEye is a distributed observability platform for Java/JVM applications providing real-time log collection, indexing, visualization, process-level monitoring, alerting, and RPC distributed tracing (Dapper-style).

## Build Commands

```bash
# Build and install all modules to local Maven repository (skip tests)
gradle clean install upload -x test

# Build specific deployable module (produces ZIP distribution)
cd skyeye-web && gradle clean distZip -x test
cd skyeye-monitor && gradle clean distZip -x test
cd skyeye-alarm && gradle clean distZip -x test

# Build collector modules
cd skyeye-collector && gradle clean build -x test

# Run tests
gradle test

# Build all Docker images
sudo bash build.sh 1.3.0 master
```

## Architecture

### Core Modules

| Module | Type | Purpose |
|--------|------|---------|
| `skyeye-base` | Library | Common constants, DTOs, utilities, Dapper span definitions |
| `skyeye-client` | Library | Log4j/Logback/Log4j2 appenders that publish to Kafka |
| `skyeye-data` | Libraries | Data access layer: JPA, HBase, Dubbo/Dubbox starters, HTTP, RabbitMQ |
| `skyeye-trace` | Library | RPC trace: distributed ID generation, sampling, tracing logic |
| `skyeye-agent` | Deployable | Lightweight agent for application deployment |

### Deployable Services

| Module | Kafka Consumer Group | Output |
|--------|---------------------|--------|
| `skyeye-collector-backup` | log-backup-consume-group | HDFS backup |
| `skyeye-collector-indexer` | es-indexer-consume-group | Elasticsearch (app logs) |
| `skyeye-collector-metrics` | info-collect-consume-group | Elasticsearch (events), RabbitMQ (alerts) |
| `skyeye-collector-trace` | rpc-trace-consume-group | HBase (RPC traces) |
| `skyeye-monitor` | - | Zookeeper-based system monitoring |
| `skyeye-alarm` | - | Email/WeChat alerts via RabbitMQ |
| `skyeye-web` | - | REST API + UI for querying logs, traces, metrics |

### Data Flow

1. **Client Libraries** (`skyeye-client`): Application logs → Kafka topic `app-log`
2. **Collector Modules**: Kafka consumers process logs based on consumer group
3. **Storage Targets**: Elasticsearch (logs/events), HBase (RPC traces), HDFS (backups)
4. **Monitoring**: `skyeye-monitor` watches Zookeeper for service changes
5. **Alerts**: `skyeye-collector-metrics` publishes to RabbitMQ → `skyeye-alarm` sends notifications

### Key Dependencies

- Kafka 0.10.0.1, Elasticsearch 2.3.3, HBase 1.0.0-cdh5.4.0
- Zookeeper 3.4.6, RabbitMQ 3.5.7
- Spring Boot 1.5.6.RELEASE, Java 1.8

### External Service Requirements

Client applications integrate via `skyeye-client` libraries and must:
- Include `kafkaAppender` in logging config pointing to Zookeeper and Kafka brokers
- Support event埋点 (logging with event types: API calls, middleware ops, jobs, third-party calls, custom logs, RPC traces)
- Register with Zookeeper for system monitoring

## Module Patterns

- **Library modules** (base, client-*, data-*, trace-*): Use `apply plugin: 'maven'`; just need `install`
- **Service modules** (alarm, monitor, web, collector-*): Use Spring Boot plugin with `mainClassName`; build `distZip`
- All modules set `buildDir = 'target'` and use UTF-8 encoding

## Known External Dependencies

- Custom Dubbox fork required for RPC tracing: `com.alibaba:dubbo:2.8.4-skyeye-trace-1.3.0`
- Elasticsearch-SQL plugin and IK analyzer required for ES 2.3.3
- Cloudera CDH versions for Hadoop/Hbase/Spark (see README for versions)