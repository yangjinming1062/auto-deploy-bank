# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **pgjdbc-ng**, a PostgreSQL JDBC driver implementation. It's a Java 1.7 project using Maven (groupId: com.impossibl, artifactId: pgjdbc-ng).

## Build Commands

```bash
mvn compile       # Compile the project
mvn test          # Run all tests (Test.java)
mvn package       # Build JAR file
```

## Architecture

### Type System (`types/` package)

The type system is central to this driver. The hierarchy includes:
- **Base** - primitive/base PostgreSQL types
- **Composite** - row types with multiple attributes
- **Domain** - types with constraints
- **Enumeration** - enum types
- **Range** - range types
- **Psuedo** - pseudo types

Each `Type` has `BinaryIO` and `TextIO` handlers for encoding/decoding:
- **BinaryIO**: `send` (Type → bytes) and `recv` (bytes → Type)
- **TextIO**: `input` (string → Type) and `output` (Type → string)

### Type Registry (`Registry.java`)

Central static registry that:
- Maps OIDs to Type instances (lazy-loaded)
- Loads type I/O handlers from `ProcProvider` instances
- Maintains type data from `pg_type`, `pg_attribute`, and `pg_proc` tables

### Procedure Providers (`system/procs/`)

`ProcProvider` interface registers I/O handlers for PostgreSQL functions. Each provider (Arrays, Bools, Bytes, Chars, Float4s, Float8s, Int2s, Int4s, Int8s, Records, Strings, UUIDs) implements handlers for type conversion functions.

### Protocol Layer (`protocol/` package)

Handles PostgreSQL wire protocol messages. The `Protocol` interface dispatches protocol messages to appropriate handlers. Message processors (e.g., `AuthenticationMP`, `DataRowMP`, `RowDescriptionMP`) handle individual message types.

### Context (`Context.java`)

Interface providing session context including:
- Type mapping (Java Class → PostgreSQL type)
- Authentication callbacks
- Result set handling callbacks
- Transaction state management

### Initialization Flow

1. `Postgres.init()` loads metadata from `pg_type`, `pg_attribute`, `pg_proc` tables
2. `Registry.update()` populates the type registry
3. Types are created on-demand via `Registry.loadType(oid)` when needed

## Key Conventions

- Uses custom `DataInputStream`/`DataOutputStream` in `utils/` for binary protocol handling
- Type categories are identified by single characters (A=Array, B=Boolean, S=String, etc.)
- ProcProvider instances are registered in `Procs.PROVIDERS` array