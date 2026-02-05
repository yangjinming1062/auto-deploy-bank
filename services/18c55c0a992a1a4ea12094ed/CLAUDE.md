# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Elkeid is an open-source Cloud Workload Protection Platform (CWPP) by ByteDance with capabilities for:
- **HIDS (Host Intrusion Detection System)** - host-level intrusion detection and malicious file identification
- **RASP (Runtime Application Self-Protection)** - dynamic injection into application runtimes
- **Kernel-level data collection** via eBPF and Kprobe hooks
- **Container and K8s security** monitoring

## Build Commands

### Agent
```bash
cd agent
BUILD_VERSION=1.7.0.24 bash build.sh
# Output: deb and rpm packages in agent/output/
```

### Server Components
```bash
cd server/agent_center && ./build.sh
cd server/service_discovery && ./build.sh
cd server/manager && ./build.sh
# Each generates bin.tar.gz in output/
```

### RASP (Runtime Application Self-Protection)
RASP requires complex toolchain. Build with native Makefile:

```bash
cd rasp
make -j$(nproc) build \
    STATIC=TRUE \
    PY_PREBUILT=TRUE \
    CC=/opt/x86_64-linux-musl-1.2.2/bin/x86_64-linux-musl-gcc \
    CXX=/opt/x86_64-linux-musl-1.2.2/bin/x86_64-linux-musl-g++ \
    LD=/opt/x86_64-linux-musl-1.2.2/bin/x86_64-linux-musl-ld \
    GNU_CC=/opt/gcc-10.4.0/bin/gcc \
    GNU_CXX=/opt/gcc-10.4.0/bin/g++ \
    VERSION=0.0.0.1
sudo make install  # Installs to /etc/elkeid/plugin/rasp
```

Or with Docker container (pre-configured toolchain):

```bash
# From rasp/ directory, with dependencies:
# - CMake 3.17+, GCC 8+, Rust 1.40+
# - MUSL toolchain 1.2.2, JDK 11+
# - PHP headers, Python2/3 headers

# Build with Docker (recommended):
curl -fsSL https://lf3-static.bytednsdoc.com/obj/eden-cn/kplrsl/ljhwZthlaukjlkulzlp/php-headers.tar.gz | tar -xz -C rasp/php
docker run --rm -v $(pwd):/Elkeid \
    -v /tmp/cache/gradle:/root/.gradle \
    -v /tmp/cache/librasp:/Elkeid/rasp/librasp/target \
    -e MAKEFLAGS="-j$(nproc)" yoloyyh/rasp-toolchain:v3.0 \
    make -C /Elkeid/rasp build \
    STATIC=TRUE \
    PY_PREBUILT=TRUE \
    CC=/opt/x86_64-linux-musl-native/bin/x86_64-linux-musl-gcc \
    GNU_CC=/opt/gcc-10.4.0/bin/gcc \
    GNU_CXX=/opt/gcc-10.4.0/bin/g++ \
    PHP_HEADERS=/Elkeid/rasp/php/php-headers \
    PYTHON2_INCLUDE=/usr/include/python2.7 \
    PYTHON3_INCLUDE=/usr/include/python3.6m

# Build output: rasp/rasp-linux-default-x86_64-*.tar.gz
```

### Driver (Kernel Module)
```bash
cd driver/LKM
make clean && make
# Produces hids_driver.ko
# For CentOS: sh ./centos_build_ko.sh

# Test:
sudo insmod hids_driver.ko
dmesg | tail -n 20
test/rst -q  # CTRL+C to quit

# Unload:
sudo rmmod hids_driver
```

**Kernel Compatibility**: 2.6.32 - 6.3
**Distro Support**: Debian 8-10, Ubuntu 14.04-20.04, CentOS 6-8, Amazon Linux 2, Alibaba Cloud Linux 3, EulerOS V2

### Go Plugins
```bash
cd plugins/{collector,driver,scanner,baseline,journal_watcher}
BUILD_VERSION=x.x.x bash build.sh
# Output: plugin_name-linux-amd64-{VERSION}.plg
```

### Rust Plugin (Driver Plugin)
```bash
cd plugins/driver
BUILD_VERSION=x.x.x bash build.sh
# Requires Rust toolchain, produces .plg files for amd64 and arm64
```

### Node.js Probe (RASP component)
```bash
cd rasp/node
npm install && npm run build
```

## Architecture

### Agent-Plugin Communication
- Agent runs as a systemd service with root privileges
- Plugins run as child processes, communicating via two pipes
- Protocol Buffers for data encoding (no double-decoding by Agent)
- Protobuf binary data is wrapped with Header feature data before server transmission

### Server Components
1. **AgentCenter (AC)** - gRPC communication with Agents, data collection → Kafka, Agent management
2. **ServiceDiscovery (SD)** - Service registration, load balancing for AC instances
3. **Manager** - Backend management API, web console backend

### Data Flow
Agent → AgentCenter → Kafka → (Elkeid HUB for rule processing) → Storage

**Transport compression**: Snappy compression is used for data transfer between Agent and AgentCenter (agent/transport/compressor/snappy.go)

### Plugin System
- Plugins are separate Go/Rust binaries spawned by Agent
- Go plugin library: `plugins/lib/go/` - provides `Client` struct for pipe communication
- Rust plugin library: `plugins/lib/rust/` - provides `PluginClient` for Rust plugins
- Common plugin structure: `plugins/{plugin_name}/`
- Plugins send binary protobuf records to Agent, receive Tasks from Agent

**Plugin protocol** (plugins/lib/bridge.proto):
- `Record`: Data record sent from plugin to Agent
- `Task`: Control task sent from Agent to plugin
- Communication via two pipes (stdin/stdout) with 4-byte length prefix + protobuf body

### RASP Components
- **librasp** - Core Rust library for process injection
- **rasp_server** - Manages RASP instances
- **agent-plugin** - RASP plugin for Agent management
- Language probes: Python, Golang, JVM, NodeJS, PHP (each has loader + probe)

## Key Dependencies

- **Go 1.18+** for agent, server, and most plugins
- **Rust** for librasp and some RASP components
- **CMake 3.17+** for RASP components
- **nFPM** for agent packaging
- **Kafka** for data pipeline
- **gRPC** with mutual TLS for agent-server communication

## Testing

Go tests exist in server components:
```bash
cd server/agent_center && go test ./...
cd server/manager && go test ./...
cd server/service_discovery && go test ./...
```

Run single test:
```bash
cd server/manager && go test -v ./internal/package -run TestName
```

Driver testing:
```bash
cd driver/LKM
insmod hids_driver.ko
test/rst -q
```

## Communication Protocol

- **Agent ↔ Server**: Bi-stream gRPC with mutual TLS (self-signed certificates)
- **Agent → Server**: Data flow (protobuf)
- **Server → Agent**: Control flow (protobuf)
- **Agent ↔ Plugins**: Pipe communication with protobuf encoding

### Driver Data Protocol
Kernel driver outputs pipe-delimited text format:
- Record separator: `\x17` (0x17)
- Field separator: `\x1e` (0x1E)
- Each record contains common fields + type-specific fields

**Common fields** (fields 1-13): data_type, uid, exe, pid, ppid, pgid, tgid, sid, comm, nodename, sessionid, pns, root_pns

**Example DataTypes**:
| Type | Name | Default |
|------|------|---------|
| 59 | execve | ON |
| 42 | connect | ON |
| 49 | bind | ON |
| 601 | dns query | ON |
| 602 | create_file | ON |
| 611 | privilege_escalation | ON |
| 701 | syscall_table_hook | ON |
| 703 | interrupt_table_hook | ON |

**Driver Filter** (`/dev/hids_driver_allowlist`):
- `Y<path>`: Add exe allowlist entry
- `F<path>`: Delete exe allowlist entry
- `W<path>`: Add write notification
- `R<path>`: Add read notification