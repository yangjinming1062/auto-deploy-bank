# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-time stock market prediction service with Kafka-based data streaming. The service consumes stock data from Kafka topics and serves predictions via REST API.

## Commands

```bash
# Install dependencies
npm install

# Run locally (requires Kafka running separately)
npm start

# Run with Docker Compose (includes Kafka and Zookeeper)
docker compose up --build

# Run in detached mode
docker compose up -d
```

## Architecture

**Service Layer** (`server.js`):
- Express.js REST API with `/` and `/health` endpoints
- Kafka consumer that subscribes to `stock-data` topic
- Processes messages via `eachMessage` handler

**Data Pipeline**:
- Kafka consumer group: `prediction-consumer-group`
- Topic: `stock-data` (configurable via `KAFKA_TOPIC`)
- Uses `kafkajs` library for Node.js

**Services** (docker-compose.yaml):
- `app`: Main prediction service (Node.js/Express)
- `kafka`: Message broker (Confluent CP-Kafka 7.5.0)
- `zookeeper`: Kafka's dependency for coordination

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Express server port |
| `KAFKA_BROKER` | localhost:9092 | Kafka broker address |
| `KAFKA_CLIENT_ID` | stock-prediction-app | Unique client identifier |
| `KAFKA_CONSUMER_GROUP` | prediction-consumer-group | Consumer group ID |
| `KAFKA_TOPIC` | stock-data | Topic to subscribe to |
| `NODE_ENV` | production | Environment mode |

## Docker Resource Limits

- App container: 1-2 CPU cores, 1-4GB memory
- Health check: `wget -q --spider http://localhost:3000/health`