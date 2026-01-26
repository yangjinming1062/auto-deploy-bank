# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZX-BT is a BitTorrent magnet search system that crawls the DHT network to discover torrent metadata and provides full-text search via a web interface. The system consists of:

- **Spider Module** (`zx-bt-spider`): DHT crawler that discovers infoHashes via UDP/TCP BitTorrent protocol
- **Web Module** (`zx-bt-web`): Spring Boot web application with search UI and real-time bullet chat (WebSocket)
- **Common Module** (`zx-bt-common`): Shared entities, enums, utilities, and Elasticsearch repository

## Build Commands

```bash
# Build all modules
mvn clean package -DskipTests

# Build specific module
mvn clean package -DskipTests -pl zx-bt-spider
mvn clean package -DskipTests -pl zx-bt-web

# Build with specific Spring Boot version
mvn clean package -DskipTests -Dzx-bt.version=1.0
```

## Architecture

### Spider Module Structure (`com.zx.bt.spider`)

The spider uses a pipeline of tasks with blocking queues for flow control:

**Tasks** (all extend AbstractTask):
- `InitTask`: Initializes UDP servers, routing tables, and Bloom filter; imports existing infoHashes from ES
- `FindNodeTask`: Continuously sends `find_node` requests to discover new nodes
- `GetPeersTask`: Sends `get_peers` requests to find peers for discovered infoHashes
- `FetchMetadataByOtherWebTask`: Attempts to fetch metadata by parsing third-party magnet sites
- `FetchMetadataByPeerTask`: Uses BEP-009 protocol over TCP to connect to peers and request metadata
- `ClearRoutingTableTask`: Periodically cleans up inactive nodes from routing tables

**UDP Protocol Processing** (socket/processor - Chain of Responsibility pattern):
- `UDPProcessorManager`: Routes messages to appropriate processor
- `Ping*`, `FindNode*`, `GetPeers*`, `AnnouncePeer*`, `Error*`: Request/response processors

**Storage**:
- `RoutingTable`: Custom Trie Tree implementation (160 levels, 8 nodes/bucket) with segmental locking for concurrent access
- `InfoHashFilter`: Guava BloomFilter for deduplication (master/slave modes for cluster deployment)

**Key Constants** (`Config.java`):
- `NODE_BYTES_LEN = 26`: 20 bytes nodeId + 4 bytes IP + 2 bytes port
- `PEER_BYTES_LEN = 6`: 4 bytes IP + 2 bytes port
- `BASIC_HASH_LEN = 20`: nodeId and infoHash length
- `METADATA_PIECE_SIZE = 16384`: 16KB pieces for metadata transfer

### Web Module Structure (`com.zx.bt.web`)

- Controllers: `IndexController`, `MetadataController`, `StatController`
- WebSocket: Real-time bullet chat functionality
- Templates: Thymeleaf-based responsive Bootstrap UI

### Common Module Structure (`com.zx.bt.common`)

- **Entity**: `Metadata` - infoHash, name, length, hot score, file list (infoString JSON)
- **Enums**: `OrderTypeEnum`, `LengthUnitEnum`, `ErrorEnum`, `CodeEnum`
- **Service**: `MetadataService` - Elasticsearch operations with Caffeine caching

## Data Flow

1. UDP servers listen on multiple ports, each with its own routing table and nodeId
2. Announce_peer/get_peers requests provide discovered infoHashes
3. InfoHash deduplicated via BloomFilter before entering processing queue
4. FetchMetadataByOtherWebTask attempts to retrieve from web sources first
5. If web fetch fails, GetPeersTask finds peers via DHT, then FetchMetadataByPeerTask connects via TCP BEP-009
6. Valid metadata indexed to Elasticsearch with IK analyzer for Chinese full-text search

## Key Configuration (application.yml)

**Spider**: `zx-bt.main.ports`, `zx-bt.performance.*`, `zx-bt.es.*`
**Web**: Server port, Elasticsearch connection, WebSocket endpoints

## Cluster Deployment

- Master node: Maintains local BloomFilter, provides `/filter` HTTP endpoint for slaves
- Slave nodes: Call master's `/filter` endpoint for deduplication instead of local filter
- Both deploy same JAR, master/slave determined by `zx-bt.main.master` config

## Important Implementation Details

- Node distance calculated via XOR of 160-bit nodeIds (closer = smaller XOR value)
- RoutingTable uses segmental locking (`locks[prefixLen % lockNum]`) for concurrency
- ISO_8859_1 encoding used for byte[] <-> String conversions to preserve raw bytes
- TCP messages must use `writeAndFlush(Unpooled.copiedBuffer(bytes))` not raw bytes
- ES field `infoString` (file metadata JSON) must use `ignore_above: 256` to avoid `超过32766字节` errors