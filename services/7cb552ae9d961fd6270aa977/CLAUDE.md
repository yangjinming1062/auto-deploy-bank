# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

zeng-rpc-framework is a hand-written RPC (Remote Procedure Call) framework implemented in Java 8. It demonstrates multiple approaches to building RPC systems including different network transports, serialization methods, compression algorithms, and service registries.

**Technology Stack:**
- Network: BIO, NIO, Netty
- Serialization: Kryo, Protostuff, Hessian, FST, JSON (Jackson/Fastjson/Gson), Protobuf, JDK
- Registry: Zookeeper (Curator), Nacos
- Proxy: JDK Dynamic Proxy, CGLIB
- Load Balancing: Random, Access Count, Consistent Hashing
- Compression: GZip, BZip2, Deflater, Lz4, Zip

## Build Commands

```bash
# Build all modules (skip tests)
mvn clean install -DskipTests

# Compile without installing
mvn clean compile

# Build a specific module
mvn -pl zyt-rpc-common clean install

# Run all tests (JUnit 5, Spring Boot Test)
mvn test

# Run a specific test class
mvn test -Dtest=ZKServiceTest

# Run with verbose output
mvn test -X
```

## Architecture Overview

### Module Structure

| Module | Purpose |
|--------|---------|
| `zyt-rpc-common` | Core utilities, entities, serialization/compression/load balancing implementations, annotations |
| `zyt-rpc-provider` | Server-side RPC implementation (Netty/NIO servers, service registration) |
| `zyt-rpc-consumer` | Client-side RPC implementation (proxies, service discovery, NIO/Netty clients) |
| `zyt-rpc-api` | User-facing API combining consumer and common modules |
| `zyt-rpc-call` | Demo module for testing client-server RPC calls |

### Key Component Patterns

**SPI-based Extensibility:**
- `META-INF/services/compress.CompressType` - Pluggable compression implementations
- `META-INF/services/consumer.proxy.ClientProxy` - Pluggable proxy implementations

**Annotation-driven Configuration:**
Use annotations on the main entry class to select implementation versions:
```java
@RpcClientBootStrap(version = "2.4")
@RpcToolsSelector(rpcTool = "Netty")
public class ClientCall { ... }
```

- `@RpcClientBootStrap(version = "2.0"-"2.4")` - Selects protocol version
- `@RpcToolsSelector(rpcTool = "Netty"/"Nio")` - Selects network transport
- `@RegistryChosen(registryName = "zookeeper"/"nacos")` - Selects registry
- `@RpcSerializationSelector(RpcSerialization = "kryo"/"protostuff"/etc)` - Selects serializer

**Bootstrap Entry Points:**
- Provider: `provider.bootstrap.netty.NettyProviderBootStrap24` (version matches @RpcClientBootStrap)
- Consumer: `consumer.bootstrap.netty.NettyConsumerBootStrap24`
- Demo: `service.ClientCall` in zyt-rpc-call module

## Core Interfaces

**Serialization:** `com.zyt.serialization.Serializer` interface with implementations in `com.zyt.serialization.*`
- Binary: Kryo, Protostuff, Hessian, FST, Protobuf
- JSON: Jackson, Fastjson, Gson

**Compression:** `com.zyt.compress.CompressType` interface implementations in `com.zyt.compress.*`
- GZip, BZip2, Deflater, Lz4, Zip

**Load Balancing:** `com.zyt.loadbalance.LoadBalance` interface
- RandomLoadBalance, AccessLoadBalance, ConsistentLoadBalance

**Client Proxy:** `com.zyt.consumer.proxy.ClientProxy` - SPI-loaded implementations for proxy pattern

**Request/Response:** `com.zyt.entity.RpcRequest` and `RpcResponse` in zyt-rpc-common