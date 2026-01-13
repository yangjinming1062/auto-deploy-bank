# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Azure Machine Learning examples repository** - a collection of examples, tutorials, and best practices for Azure ML services and features. The repository demonstrates how to use Azure ML SDK v2 and CLI v2 across multiple programming languages.

## Repository Structure

The repository is organized by developer experience:

- **`cli/`** - Azure ML CLI (v2) examples with YAML-based job definitions
  - Examples organized by: endpoints, jobs (single-step/pipelines), schedules, assets
  - Contains bash scripts for common operations
  - Each example has auto-generated README with status badges

- **`sdk/`** - SDK examples across languages
  - **`python/`** - Most extensive, with examples for MLflow, MLTable, AutoML, jobs, pipelines
  - **`dotnet/`** - .NET SDK v2 examples
  - **`typescript/`** - TypeScript SDK v2 examples

- **`tutorials/`** - End-to-end tutorials and getting started guides
  - Notebook-based tutorials with step-by-step instructions

- **`best-practices/`** - Deep learning best practices and patterns
  - Distributed training examples (DeepSpeed, Nebula)
  - Operationalization patterns
  - Environment management

- **`infra/`** - Infrastructure templates and bootstrapping scripts
  - ARM templates for resource deployment
  - Validation scripts

## Common Development Commands

### Setup

```bash
# Install dev dependencies (from repository root)
pip install -r dev-requirements.txt

# Install pre-commit hooks
pre-commit install

# Set up CLI (if working with CLI examples)
cd cli && ./setup.sh

# Set up Python SDK (if working with SDK examples)
cd sdk/python && ./setup.sh
```

### Code Formatting and Linting

```bash
# Format all Python code and notebooks (required before PRs)
black .
black-nb .

# Run pre-commit checks
pre-commit run --all-files
```

### Running Examples

```bash
# Run a CLI job
az ml job create -f cli/jobs/single-step/pytorch/iris/job.yml

# Run a pipeline
bash cli/run-pipeline-jobs.sh

# Run all jobs in a directory
python cli/run-job-pipeline-all.py
```

### Generating Documentation

```bash
# Auto-generate README.md files with example listings (run in respective subdirectory)
cd cli && python readme.py
cd sdk/python && python readme.py
cd tutorials && python readme.py

# This also generates GitHub Actions workflow files for testing
```

### Testing

Examples are automatically tested via GitHub Actions workflows (`.github/workflows/`). Most examples have corresponding workflow files that:
- Test CLI commands
- Validate YAML syntax
- Run example jobs on Azure ML compute clusters

PRs from forks may fail automated workflows due to secret access limitations.

## Key Patterns and Conventions

### YAML Job Schema

Azure ML CLI examples use YAML job definitions with this schema:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
code: src                          # Source code directory
command: >-                       # Command to run
  pip install -r requirements.txt &&
  python main.py --data ${{inputs.data}}
inputs:                           # Input parameters
  data:
    type: uri_file
    path: https://example.com/data.csv
  epochs: 10                      # Scalar input with default
environment: azureml://registries/azureml/environments/sklearn-1.5/labels/latest
compute: azureml:cpu-cluster      # Compute target
experiment_name: my-experiment
description: Example description
```

**YAML section order**: `code > command > inputs > environment > compute > experiment_name > description`

### Example Directory Structure

```
cli/jobs/single-step/pytorch/iris/
├── job.yml                      # Job definition
└── src/                         # Source code
    ├── main.py                  # Entry point
    ├── network.py               # Model definition
    └── requirements.txt         # Dependencies
```

### Data and Environment Patterns

- **Data**: Prefer public cloud data URLs (Azure blob storage, HTTPS)
- **Environments**: Use Azure ML curated environments when possible
- **Compute**: Use existing compute clusters defined in `setup.sh`
- **Inline definitions**: Keep environment and data definitions inline in YAML

### Scripts and Deployment

- All shell scripts run with `bash -x` (prints each command)
- **Security**: Wrap sensitive commands with `set +x` / `set -x` to suppress output
- Use GitHub secrets for confidential data
- Bash scripts often used as source for MicrosoftDocs/azure-docs code snippets

## Important Notes from Documentation

### File Ownership (`.github/copilot-instructions.md`)

Files owned by `@azure/ai-platform-docs` in CODEOWNERS have special restrictions:
- Do not change filenames or move files
- Do not remove comments containing `<text>` or `</text>` tags
- Do not remove notebook cells with `name:` metadata
- Contact the AI Platform Docs team for approval before these changes

### Contributing Guidelines (`.github/PULL_REQUEST_TEMPLATE.md`)

- PRs require Azure ML team review and approval
- Run `black` and `black-nb` before submitting
- Regenerate README.md files with `python readme.py`
- Add compute cluster names to `sdk/python/notebooks_config.ini` for cleanup
- Include YAML frontmatter in new example READMEs:

```yaml
---
page_type: sample
languages:
- azurecli
- language1
- language2
products:
- azure-machine-learning
description: Example description.
---
```

### Development Limitations

- This is an examples repository, **not reference documentation**
- Reference docs go in [azure-sdk-for-python](https://github.com/Azure/azure-sdk-for-python)
- Long-form documentation goes in [azure-docs](https://github.com/MicrosoftDocs/azure-docs)

## Additional Resources

- [Azure ML Documentation](https://docs.microsoft.com/azure/machine-learning)
- [Azure ML Python SDK v2 Overview](https://learn.microsoft.com/azure/machine-learning/concept-v2)
- [Azure CLI ML Extension v2](https://learn.microsoft.com/azure/machine-learning/concept-v2)