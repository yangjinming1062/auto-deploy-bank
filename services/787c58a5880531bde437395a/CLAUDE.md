# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simplify is a generic Android deobfuscator that virtually executes Dalvik bytecode to understand app behavior, then applies optimizations to produce cleaner, equivalent code. The project has three main modules:

- **smalivm**: Virtual machine sandbox for executing Dalvik methods, returning execution graphs with all possible register/class values per path
- **simplify**: Optimization engine that applies constant propagation, dead code removal, unreflection, and peephole optimizations
- **demoapp**: Example usage of smalivm API

## Build Commands

```bash
# Run all tests
./gradlew test

# Build standalone JAR with all dependencies
./gradlew fatjar

# Build smalivm JAR only
./gradlew :smalivm:fatjar

# Run a single test class
./gradlew test --tests "org.cf.smalivm.*"
./gradlew :simplify:test --tests "org.cf.simplify.strategy.*"
```

## Architecture

### smalivm (Virtual Machine)

Core execution flow: `VirtualMachine` → `MethodExecutor` → `NodeExecutor` → `Op` implementations

**Key packages:**
- `context/`: Execution state management
  - `ExecutionGraph`: Contains all `ExecutionNode`s representing possible execution paths; tracks register values and class states
  - `ExecutionNode`: Single point in execution with associated `Op` and `ExecutionContext`
  - `ExecutionContext`: Holds `MethodState` (register values) and `ClassState` (field values) for a specific path
  - `MethodState`: Tracks register assignments and stack values
  - `ClassState`: Tracks static field values for a class
- `opcode/`: Dalvik instruction implementations
  - Each `Op` subclass handles a specific opcode (InvokeOp, ConstOp, IfOp, etc.)
  - `OpFactory` pattern: `*Op` classes with corresponding `*OpFactory` for creation
  - `Op.execute()` updates `ExecutionNode` children based on instruction behavior
- `type/`: Type system for virtual execution
  - `VirtualType`: Base type representation
  - `VirtualClass`: Class metadata with fields and methods
  - `VirtualMethod`: Method descriptor and implementation
- `dex/`: DEX file handling via smali/dexlib2
  - `ClassBuilder`: Constructs `VirtualClass` instances from DEX
  - `SmaliClassLoader`: Loads smali classes for reflection

**Execution model:**
- Uses "multiverse execution" - explores all branches when conditions are unknown
- `ExecutionGraph` contains `ExecutionNode` piles (template node + concrete nodes) at each address
- `MethodExecutor` uses a work queue (`ArrayDeque`) to traverse nodes breadth-first

### simplify (Optimization Engine)

**Key classes:**
- `Launcher`: Entry point, handles CLI arguments and orchestrates optimization
- `Optimizer`: Runs optimization passes repeatedly until no changes
- `ExecutionGraphManipulator`: Modifies `ExecutionGraph` instances in-place
- `ConstantBuilder`: Constructs constant values from consensus register values

**Optimization strategies** (`strategy/`):
1. `ConstantPropagationStrategy`: Replaces ops with constant values when all paths agree
2. `DeadRemovalStrategy`: Removes ops with no side effects and unused register assignments
3. `UnreflectionStrategy`: Replaces `Method.invoke()`/`Field.get()` calls with direct calls when possible
4. `PeepholeStrategy`: Local optimizations (check-cast removal, string init optimization)

**Optimization flow:**
1. Load DEX and build `ExecutionGraph` via `VirtualMachine.spawnInstructionGraph()`
2. `Optimizer` iterates, applying strategies until no changes or max passes
3. Each strategy modifies `ExecutionGraphManipulator`, which updates the graph
4. When optimizations complete, write modified DEX via dexlib2

## Important Conventions

- `ExecutionGraph` has two states: template (from `spawnInstructionGraph`) and concrete (from `execute`)
- Consensus values: When all nodes at an address agree on a register value, that value is the "consensus"
- Side effects: Operations are only removable if `SideEffect.Level` is below threshold
- Unknown values: Represented by `UnknownValue` type; any operation on unknown propagates uncertainty

## Dependency Notes

- smalivm uses dexlib2/smali for DEX parsing and smali assembly
- Android framework classes (android.util.Base64, etc.) are reflected rather than virtually executed
- Framework JAR at `smalivm/src/main/resources/framework/android-framework.jar` contains reference classes