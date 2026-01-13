# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FIND3 (Framework for Internal Navigation and Discovery) v3.x is an indoor positioning system that uses machine learning to determine location based on sensor data (Bluetooth, WiFi, magnetic fields, etc.). It's a complete re-write with support for multiple data sources, passive scanning, and 10 different ML classifiers.

## Architecture

The project has a three-tier architecture:

1. **Data Server** (`server/main/`): Go-based HTTP server (Gin framework) that stores sensor fingerprints in SQLite databases and provides REST API endpoints
   - Port: 8003 (default)
   - WebSocket support for real-time updates
   - Static frontend with HTML templates
   - MQTT integration for message queuing

2. **AI Server** (`server/ai/`): Python/Flask machine learning server that performs classification and learning
   - Port: 8002 (default)
   - 10 different ML classifiers (Random Forest, Neural Networks, etc.)
   - Flask API endpoints for `/learn` and `/classify` operations

3. **Documentation Server** (`doc/`): Go-based static documentation server
   - Port: 9999
   - Serves markdown documentation

## Key Code Locations

- **`server/main/main.go`**: Entry point for data server with flag configuration
- **`server/main/src/server/server.go`**: Main HTTP router and web UI handlers
- **`server/main/src/database/db.go`**: SQLite database operations (fingerprints, locations, predictions)
- **`server/main/src/api/`**: API handlers for `/track` and `/learn` endpoints
- **`server/main/src/models/`**: Data models (SensorData, LocationAnalysis)
- **`server/main/src/learning/nb1/` & `nb2/`**: Naive Bayes classifier implementations
- **`server/main/src/mqtt/mqtt.go`**: MQTT client for message queuing

## Common Development Commands

### Building and Running

```bash
# Build and run data server in debug mode
cd server/main
make server1

# Or manually
go build -v
./main -debug

# Run with custom ports
./main -debug -port 8003 -ai 8002

# Run AI server in development mode
cd server/ai
make serve

# Run AI server in production mode
cd server/ai
make production

# Build and run documentation server
cd doc
go run *.go
# Or from root: make docs

# Install AI server dependencies
cd server/ai
make install
```

### Testing

```bash
# Run all Go tests
cd server/main
go test ./...

# Run tests with verbose output
go test -v ./...

# Run specific test file
go test -v ./src/api/calibration_test.go
go test -v ./src/database/db_test.go

# Run AI server tests (requires dependencies)
cd server/ai
make test
```

### Database Operations

```bash
# Dump a family database to JSON
./main -dump <family_name>

# Database location (configurable with -data flag)
# Default: ./data/
```

### Docker

```bash
# Build Docker image
docker build -t find3 .

# Run with volume mounts
docker run -p 11883:1883 -p 8003:8003 -v /tmp/find3:/data -t find3

# The Docker container runs both main and AI servers via supervisord
```

### Dependency Management

```bash
# Update Go dependencies (uses dep)
cd server/main
make update

# The project uses dep for Go dependency management
# See go.mod for full dependency list
```

## Configuration Flags

Data server flags (`server/main/main.go`):
- `-ai`: AI server port (default: 8002)
- `-port`: Data server port (default: 8003)
- `-debug`: Enable debug logging
- `-data`: Data storage directory (default: ./data)
- `-mqtt-server`: MQTT server address
- `-mqtt-admin`: MQTT admin username (default: admin)
- `-mqtt-pass`: MQTT admin password (default: 1234)
- `-mqtt-dir`: MQTT config directory (default: mosquitto_config)
- `-dump`: Dump specified family database to JSON
- `-memprofile`: Enable memory profiling
- `-cpuprofile`: Enable CPU profiling

## API Endpoints

### Main Server (Port 8003)
- `GET/POST /`: Login page and authentication
- `POST /track`: Submit sensor data for real-time tracking
- `POST /learn`: Submit sensor data for training/learning
- `GET /view/analysis/:family`: View location analysis dashboard
- `GET /view/dashboard/:family`: View family dashboard
- `GET /api/v1/locations/:family`: Get locations for family
- `GET /api/v1/last/:family/:location`: Get last data for location
- `DELETE /api/v1/database/:family`: Delete entire family database
- `DELETE /api/v1/location/:family/:location`: Delete specific location
- `WebSocket /`: Real-time predictions and updates

### AI Server (Port 8002)
- `POST /learn`: Train ML models with sensor data
- `POST /classify`: Classify sensor data to predict location
- `GET /`: Health check endpoint

## Data Models

Key structures in `server/main/src/models/`:
- **SensorData**: Input data structure with timestamp, device, location, and sensor readings
- **LocationAnalysis**: Prediction results with confidence scores
- **GPS**: Geolocation data (latitude, longitude, altitude)

## Testing Resources

- **`server/main/testing/`**: Contains test data and scripts
  - `testdb.learn.1439597065993.jsons`: Sample learning data
  - `submit_jsons.py`: Python script to submit test data
  - `learn.sh`: Shell script for testing

## Important Files

- **`go.mod`**: Go module dependencies
- **`Dockerfile`**: Multi-stage build for production deployment
- **`Makefile`**: Build targets for main server
- **`server/main/src/server/server.go`**: HTTP server setup and routing
- **`server/main/src/database/db.go`**: Database schema and operations
- **`runner.conf`**: Live-reload configuration for development

## Development Notes

- Uses SQLite for data persistence (no external DB required)
- Rolling compression of MAC addresses via `stringsizer` library
- WebSocket-based real-time updates reduce bandwidth
- Automatic recalibration triggered after 5+ fingerprints (debounced)
- MQTT integration enables distributed sensor collection
- Static assets served from `server/main/static/`
- Templates served from `server/main/templates/`

## Database Schema

SQLite database per family with tables:
- `keystore`: Key-value store for metadata
- `sensors`: Sensor fingerprint data (timestamp, device, location, dynamic columns)
- `location_predictions`: Prediction results over time
- `devices`: Device registry
- `locations`: Location registry
- `gps`: GPS coordinate data

## Deployment

The production deployment uses:
- Docker with supervisord to run both servers
- Mosquitto MQTT broker
- Data persistence via volume mount to `/data`
- Multiple architecture support (amd64, arm, etc.)