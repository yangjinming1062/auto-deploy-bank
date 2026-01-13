# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vespa is a distributed big data platform for serving, searching, and performing inference on vectors, tensors, text, and structured data at serving time and any scale. It's a production-grade, high-performance platform used by major internet services to serve hundreds of thousands of queries per second.

**Architecture**: ~150 modules in a flat structure with equal parts Java (~50%) and C++ (~50%), totaling ~1.7M lines of code.

## Common Commands

### Build Commands

```bash
# Full build (recommended)
./bootstrap.sh full
mvn install --threads 1C

# Java-only build
./bootstrap.sh java
mvn install --threads 1C

# Quick Java build
./quickbuild.sh

# CMake build (after Java bootstrap)
cmake -S . -B build
cmake --build build
```

### Test Commands

```bash
# All tests
mvn install --threads 1C

# Skip tests during build
mvn install --threads 1C -DskipTests

# Run specific test
mvn test -Dtest=ClassName

# Shell script tests (BATS)
bats -r .

# Go client tests
cd client/go && make test

# JS client tests
cd client/js/app && npm test
```

### Build Tools Requirements

- **CMake**: 3.20+ (for C++ build)
- **Maven**: 3.9.9 with wrapper (mvnvm.properties)
- **JDK**: 17 (.java-version)
- **Go**: 1.24 (toolchain 1.24.2) for client tools
- **Node.js**: For shell tests (BATS framework)

### Development Environment

**Docker-based Development (Recommended)**:
Follow the guide at [Vespa development on AlmaLinux 8](https://github.com/vespa-engine/docker-image-dev#vespa-development-on-almalinux-8) for a complete environment.

**Mac Setup**:
```bash
# Install dependencies
brew install jenv mvnvm openjdk@17

# Intel compatibility on ARM Macs (for grpc)
softwareupdate --install-rosetta

# Symlink JDK
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

# Configure jEnv
echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(jenv init -)"' >> ~/.zshrc
eval "$(jenv init -)"
jenv enable-plugin export
exec $SHELL -l
jenv add $(/usr/libexec/java_home -v 17)
```

## Architecture Overview

Vespa follows a layered architecture with three main subsystems:

```
┌─────────────────────────────────────────┐
│         Stateless Container (Java)       │
│  ┌─────────────┐ ┌─────────────────────┐ │
│  │ jDisc Core  │ │   Container Layer   │ │
│  │ (HTTP/REST) │ │  (OSGi, DI, Metrics)│ │
│  └─────────────┘ └─────────────────────┘ │
│  ┌─────────────┐ ┌─────────────────────┐ │
│  │  Container  │ │    Document         │ │
│  │   Search    │ │   Processors        │ │
│  └─────────────┘ └─────────────────────┘ │
├─────────────────────────────────────────┤
│         Content Nodes (C++)              │
│  ┌─────────────┐ ┌─────────────────────┐ │
│  │ Search Core │ │     Storage         │ │
│  │ (Proton)    │ │  (Distributed)      │ │
│  └─────────────┘ └─────────────────────┘ │
│  ┌─────────────┐ ┌─────────────────────┐ │
│  │    Search   │ │   Cluster           │ │
│  │     Lib     │ │   Controller        │ │
│  └─────────────┘ └─────────────────────┘ │
├─────────────────────────────────────────┤
│    Config & Admin (Java)                 │
│  ┌─────────────┐ ┌─────────────────────┐ │
│  │Config Server│ │   Config Model      │ │
│  │(Deployment) │ │(Application Model)  │ │
│  └─────────────┘ └─────────────────────┘ │
└─────────────────────────────────────────┘
```

### Core Modules

**Stateless Container (Java)**:
- `jdisc_core/` - HTTP server, protocol handling, request-response framework
- `container-core/` - OSGi, dependency injection, metrics, HTTP connector
- `container-search/` - Query/Result processing, Searcher framework, query profiles
- `document/` - Document model (Java + C++)
- `messagebus/` - Async messaging (Java + C++)
- `docproc/` - Document processing chains
- `indexinglanguage/` - Indexing expression compiler
- `documentapi/` - Document operation APIs

**Content Layer (C++)**:
- `searchcore/` - Proton search engine, indexing, matching, ranking, storage
- `searchlib/` - Ranking frameworks, FEF, rank features, indexes, attributes
- `storage/` - Distributed storage system (elastic, auto-recovery)
- `eval/` - Tensor operations and ranking expression evaluation
- `storageapi/` - Storage message bus implementation

**Configuration & Admin (Java)**:
- `configserver/` - Central deployment server
- `config-model/` - Application system model
- `config/` - Config subscription library (Java + C++)
- `configgen/` - Config class generation
- `clustercontroller-core/` - Storage cluster controller

**Utility Libraries**:
- `vespalib/` - C++ utilities
- `vespajlib/` - Java utilities
- `client/go/` - CLI client (Go)
- `client/js/app/` - Web UI (React)

### Module Hierarchy

The flat module structure is organized by dependency layers:
1. **Foundation**: `vespalib`, `vespajlib`, `config`
2. **Content**: `searchcore`, `searchlib`, `storage`, `eval`
3. **Container**: `jdisc_core`, `container-core`, `component`
4. **Services**: `container-search`, `docproc`, `messagebus`
5. **Administration**: `configserver`, `config-model`

## Development Workflow

### Open Development Model
- All work via GitHub Pull Requests using GitHub flow
- Master branch released 4x/week (Monday-Thursday)
- All PRs must be approved by a Vespa Committer
- Check OWNERS files for appropriate reviewers
- Continuous build at [factory.vespa.ai](https://factory.vespa.ai)

### Versioning & Compatibility
- Semantic versioning with strict ABI compatibility
- Java APIs with `@PublicAPI` (non-`@Beta`) annotation cannot change incompatibly between major versions
- ABI compatibility verified during Maven build
- Update ABI spec if adding to public APIs (build will fail with instructions)

### Release Process
- New releases from master branch daily (Mon-Thu)
- Version tags: `v*.*.*`
- All changes via PR with review required
- Code must maintain backwards compatibility

### Contribution Process
1. Check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
2. Create PR with appropriate OWNER approval
3. Ensure all tests pass
4. Maintain API compatibility
5. Follow [Code-map.md](Code-map.md) to understand module structure

## Key Build Files

- `pom.xml` - Maven parent POM (140+ modules)
- `CMakeLists.txt` - Main CMake configuration
- `functions.cmake` - Custom CMake functions
- `bootstrap.sh` - Build initialization script
- `quickbuild.sh` - Fast Java build
- `.java-version` - JDK 17
- `mvnvm.properties` - Maven 3.9.9

## Testing Framework

### Language-Specific Testing
- **C++**: Google Test (GTest) with CTest
- **Java**: JUnit with Maven Surefire
- **Shell**: BATS (Bash Automated Testing System)
- **Go**: Go test framework
- **JavaScript**: Vitest

### Test Organization
- C++: `<module>/src/tests/`, `*_test_app`
- Java: `src/test/java/`
- Shell: Root-level `.bats` files
- Integration tests: `integration/` directory

## Code Style & Quality

### JavaScript/TypeScript (client/js/app/)
- **ESLint 9.x** with comprehensive plugin set:
  - eslint-plugin-import, eslint-plugin-prettier
  - eslint-plugin-react, eslint-plugin-react-hooks
  - eslint-plugin-react-perf, eslint-plugin-unused-imports
- **Prettier 3.x** for formatting
- **Husky** for git hooks

### Other Languages
- **C++**: Compiler warnings (Wall, Wextra), sanitizers (Valgrind, TSAN, UBSAN)
- **Java**: Maven Enforcer plugin, dependency convergence checks
- **Go**: `gofmt`, `go vet`, `checkfmt` target
- **Shell**: ShellCheck integration

## Important Resources

- **Documentation**: [https://docs.vespa.ai](https://docs.vespa.ai)
- **Homepage**: [https://vespa.ai](https://vespa.ai)
- **Sample Apps**: [https://github.com/vespa-engine/sample-apps](https://github.com/vespa-engine/sample-apps)
- **System Tests**: [https://github.com/vespa-engine/system-test](https://github.com/vespa-engine/system-test)
- **Documentation Repo**: [https://github.com/vespa-engine/documentation](https://github.com/vespa-engine/documentation)
- **Build Status**: [https://factory.vespa.ai](https://factory.vespa.ai)
- **Slack Community**: [https://slack.vespa.ai](https://slack.vespa.ai)

## Finding Your Way Around

### For Architecture Understanding
- Read [Code-map.md](Code-map.md) for functional overview
- Check individual module READMEs (~50+ modules have them)
- See [README.md](README.md) for project overview

### For Contributions
- See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow
- Check [GOVERNANCE.md](GOVERNANCE.md) for committer process
- Review [TODO.md](TODO.md) for suggested improvements
- Consult [OWNERS](OWNERS) files for code ownership

### For Development
- Use Docker development environment for consistency
- All platform-specific setup in README.md
- Build logs and issues at [factory.vespa.ai](https://factory.vespa.ai)

## License

All code licensed under Apache 2.0 (see [LICENSE](LICENSE) file).