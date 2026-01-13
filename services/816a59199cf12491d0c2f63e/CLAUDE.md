# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

SkyPilot is a framework for running AI and batch workloads on any infrastructure, offering unified execution, high cost savings, and high GPU availability. It abstracts away infrastructure burdens by allowing users to launch clusters, jobs, and services on any cloud or Kubernetes cluster.

The core of SkyPilot is a YAML or Python interface that defines a task's resource requirements, data synchronization, setup commands, and task commands. SkyPilot then handles the heavy lifting of finding the best-priced infrastructure, provisioning it, syncing the code, and running the job.

## Common Commands

### Installation

To install SkyPilot for development:

```bash
# Install for all clouds
pip install -e ".[all]"
pip install -r requirements-dev.txt
```

### Testing

To run smoke tests:

```bash
# Run all tests except for AWS and Lambda Cloud
pytest tests/test_smoke.py

# Run a single test
pytest tests/test_smoke.py::test_minimal

# Only run managed spot tests
pytest tests/test_smoke.py --managed-spot

# Run tests for a specific cloud
pytest tests/test_smoke.py --aws
```

### Formatting

To format the code:

```bash
./format.sh
```
