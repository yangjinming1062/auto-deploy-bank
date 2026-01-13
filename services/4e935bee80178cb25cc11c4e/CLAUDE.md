# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**guide-rpc-framework** is a custom RPC framework implementation based on Netty + Kryo + Zookeeper. The framework provides high-performance remote procedure calls with service discovery, load balancing, multiple serialization options, and Spring integration.

## Architecture

The project is a Maven multi-module structure:

- **`rpc-framework-simple`**: Core RPC framework implementation (46 source files)
  - `remoting/`: Network transport layer (Netty and Socket implementations)
  - `registry/`: Service registration/discovery (Zookeeper-based)
  - `serialize/`: Multiple serialization strategies (Kryo, Hessian, Protostuff)
  - `loadbalance/`: Load balancing algorithms (Random, ConsistentHash)
  - `proxy/`: Dynamic proxy for client-side invocation
  - `compress/`: Compression support (Gzip)
  - `annotation/`: Core annotations (@RpcService, @RpcReference, @RpcScan)
  - `provider/`: Service provider management
  - `spring/`: Spring integration

- **`rpc-framework-common`**: Shared utilities and constants
  - `extension/`: SPI mechanism (ExtensionLoader) similar to Dubbo
  - `enums/`: Configuration and status enums
  - `utils/`: Utility classes (String, Collection, ThreadPool, etc.)
  - `factory/`: SingletonFactory for instance management
  - `exception/`: Custom exceptions (RpcException, SerializeException)

- **`hello-service-api`**: Example service interfaces and DTOs
- **`example-server`**: Service provider implementation and bootstrap
- **`example-client`**: Service consumer implementation and bootstrap

### Core Flow

1. **Service Registration**: Server registers service with Zookeeper via `@RpcService` annotation
2. **Service Discovery**: Client discovers services from Zookeeper via `@RpcReference` annotation
3. **Request Flow**: Client proxy → Load balancer → Netty client → Network → Netty server → Service handler
4. **Response Flow**: Result → Serialization → Compression → Network → Deserialization → Client future completion

## Common Commands

### Build & Test
```bash
# Build all modules
mvn clean install

# Run tests for all modules
mvn test

# Run tests for specific module
cd rpc-framework-simple && mvn test

# Run single test class
mvn test -Dtest=ConsistentHashLoadBalanceTest

# Skip tests during build
mvn clean install -DskipTests
```

### Development Workflow
```bash
# Clean and rebuild after changes
mvn clean install -DskipTests

# Run static analysis (if configured)
mvn checkstyle:check

# Package without running tests
mvn package -DskipTests
```

### Running the Examples

**Prerequisites**:
- Zookeeper 3.5.8+ running on 127.0.0.1:2181

```bash
# Start Zookeeper via Docker
docker run -d --name zookeeper -p 2181:2181 zookeeper:3.5.8

# 1. Build the project
mvn clean install

# 2. Start the server (in one terminal)
cd example-server
mvn exec:java -Dexec.mainClass="NettyServerMain"

# 3. Start the client (in another terminal)
cd example-client
mvn exec:java -Dexec.mainClass="NettyClientMain"

# Alternative: Run directly from IDE
# - Run example-server/src/main/java/NettyServerMain
# - Run example-client/src/main/java/NettyClientMain
```

## Key Components

### Annotations
- **`@RpcService`**: Marks service implementation (server-side)
  - Parameters: `version`, `group`
- **`@RpcReference`**: Injects remote service reference (client-side)
  - Parameters: `version`, `group`
- **`@RpcScan`**: Enables component scanning
  - Parameters: `basePackage[]`

### Protocol Structure
The custom protocol uses a 16-byte header:
- Magic number: `grpc` (4 bytes)
- Version: 1 byte
- Message type: 1 byte (REQUEST/RESPONSE/HEARTBEAT)
- Serialization type: 1 byte
- Compress type: 1 byte
- Request ID: 8 bytes
- Total length: 4 bytes

### SPI Extension Points
Located in `META-INF/extensions/`:
- **Serializer**: `kryo`, `hessian`, `protostuff`
- **LoadBalancer**: `random`, `consistentHash`
- **ServiceRegistry**: `zk`
- **ServiceDiscovery**: `zk`
- **RpcRequestTransport**: `netty`, `socket`

### Configuration
Default configurations in `RpcConstants`:
- Zookeeper address: `127.0.0.1:2181`
- Default serialization: `kryo`
- Heartbeat interval: Configurable via `IdleStateHandler`
- Magic number: `0x67727063` ("grpc")

## Testing

Test locations:
- `rpc-framework-simple/src/test/java/`
- `rpc-framework-common/src/test/java/`

Available test classes:
- `KryoSerializerTest`
- `HessianSerializerTest`
- `ZkServiceRegistryImplTest`
- `ConsistentHashLoadBalanceTest`
- `GzipCompressTest`
- `ExtentionTest`

Run tests with Maven Surefire plugin configured in POMs.

## Module Dependencies

```
rpc-framework-simple
├── rpc-framework-common (compile)
└── hello-service-api (compile)

example-server
├── rpc-framework-simple (runtime)
└── hello-service-api (compile)

example-client
├── rpc-framework-simple (runtime)
└── hello-service-api (compile)
```

## Important Files

### Core Framework
- `rpc-framework-simple/src/main/java/github/javaguide/remoting/transport/netty/`: Netty client/server implementations
- `rpc-framework-simple/src/main/java/github/javaguide/registry/zk/`: Zookeeper integration
- `rpc-framework-simple/src/main/java/github/javaguide/proxy/RpcClientProxy.java`: Dynamic proxy implementation
- `rpc-framework-simple/src/main/java/github/javaguide/spring/`: Spring integration beans

### Configuration
- `pom.xml`: Root Maven POM with dependency versions
- `rpc-framework-simple/pom.xml`: Core module dependencies
- `rpc-framework-common/src/main/java/github/javaguide/enums/`: Configuration enums

### Examples
- `example-server/src/main/java/NettyServerMain.java`: Server bootstrap
- `example-client/src/main/java/NettyClientMain.java`: Client bootstrap
- `example-server/src/main/java/github/javaguide/serviceimpl/HelloServiceImpl.java`: Service implementation

## Performance Optimizations Implemented

- **Channel Reuse**: Netty channels are cached and reused across requests
- **CompletableFuture**: Async response handling without blocking threads
- **Connection Pooling**: ChannelProvider manages client connections
- **Gzip Compression**: Reduces network payload size
- **Heartbeat Mechanism**: Maintains long-lived connections
- **Selective Serialization**: Configurable per-service serializer

## Future Enhancement Areas (from README)

- [ ] Configuration externalization (currently some hardcoded values)
- [ ] Comprehensive test suite for all modules
- [ ] Service monitoring/management console
- [ ] Additional load balancing strategies (round-robin, least-connections)
- [ ] Circuit breaker and fault tolerance mechanisms
- [ ] Metrics and tracing integration

## Development Notes

- Uses Java 8 with Lombok (annotations processed at compile time)
- Netty 4.1.42 for NIO-based networking
- Curator 4.2.0 for Zookeeper client operations
- Spring 5.2.7 for dependency injection and annotation processing
- JUnit 5 for testing

## Troubleshooting

**Zookeeper Connection Issues**:
```bash
# Check if Zookeeper is running
docker ps | grep zookeeper
# Restart Zookeeper
docker restart zookeeper
```

**Port Conflicts**:
- Default Netty port: Check `NettyRpcServer` configuration
- Zookeeper port: 2181 (configurable)

**ClassNotFoundException**:
```bash
# Ensure all modules are built
mvn clean install -DskipTests
```

**Test Failures**:
- Tests may require Zookeeper to be running
- Check test-specific configuration in `src/test/resources/`