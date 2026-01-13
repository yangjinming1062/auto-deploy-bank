# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

The following commands are available in the `Makefile` and are commonly used for development:

*   `make conf`: Install dependencies.
*   `make dev`: Install development dependencies.
*   `make valid`: Run all validation checks (linting, formatting, etc.).
*   `make check`: Run all validation checks.
*   `make test`: Run the test suite.
*   `make doc`: Build the documentation.
*   `make run`: Run the development server.

## High-level Code Architecture

The core of ScanCode.io is the **ScanPipe** framework, which is a modular and extensible system for automating software composition analysis.

### Key Concepts

*   **Projects**: A `Project` encapsulates the analysis of a codebase. Each project has its own workspace, which includes directories for input files, the extracted codebase, output files, and temporary files.

*   **Pipelines**: `Pipelines` are Python scripts that define a series of steps for analyzing a codebase. Each step is a method on the `Pipeline` class. The order of execution is defined in the `steps` class attribute. Built-in pipelines are located in the `scanpipe/pipelines` directory.

*   **Pipes**: `Pipes` are the building blocks of pipelines. They are functions that perform specific, reusable tasks, such as collecting codebase resources, scanning for packages, or generating reports. Pipes are located in the `scanpipe/pipes` directory.

*   **Codebase Resources**: A `CodebaseResource` represents a file or directory in the codebase being analyzed. It stores metadata about the resource, such as its status, type, and any discovered licenses or copyrights.

*   **Discovered Packages**: A `DiscoveredPackage` represents a software package (e.g., a Debian package, a PyPI package) that has been discovered in the codebase. It stores information about the package, such as its name, version, and license.

### Extensibility

ScanCode.io is designed to be extensible. You can create custom pipelines to add new analysis capabilities or to modify the behavior of existing pipelines. Custom pipelines can be added to the directories defined in the `SCANCODEIO_PIPELINES_DIRS` setting.
