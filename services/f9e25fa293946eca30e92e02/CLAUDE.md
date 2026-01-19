# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

### Development Commands

The project uses **make** for most development tasks. Key commands:

```bash
# Build Docker image
make build

# Run miner (mainnet)
make miner WALLET_NAME=<name> WALLET_HOTKEY=<hotkey>

# Run validator (mainnet)
make validator WALLET_NAME=<name> WALLET_HOTKEY=<hotkey>

# Run on testnet (netuid 118)
make test-miner WALLET_NAME=<name> WALLET_HOTKEY=<hotkey>
make test-validator WALLET_NAME=<name> WALLET_HOTKEY=<hotkey>

# Run locally (staging)
make local-miner
make local-validator

# Debug with remote debugger (port 5678)
make debug-local-miner
make debug-local-validator
make debug-test-miner
make debug-test-validator
make debug-finney-validator

# View logs
make miner-logs
make validator-logs

# Clean up
make stop
make clean
```

### Linting & Formatting

**Setup:** Pre-commit hooks are configured. Install with:
```bash
pre-commit install
```

**Manual linting:**
```bash
# Black formatting
black neurons/

# Flake8 linting
flake8 neurons/

# isort import sorting
isort neurons/
```

**Test configuration:** Python 3.12, pytest configured in `pyproject.toml` with test paths in `tests/` directory.

### Python Environment

- **Package manager:** uv
- **Python version:** 3.12
- **Dependencies:** See `requirements.txt` and `pyproject.toml`

Key dependencies include:
- bittensor==9.9.0 (blockchain network)
- ezkl==22.0.1 (zero-knowledge proofs)
- torch==2.7.1 (ML framework)
- onnxruntime>=1.21.0 (ONNX execution)
- fastapi==0.110.3 (API framework)
- uvicorn==0.34.0 (ASGI server)

### Networks

- **Mainnet:** `--subtensor.network finney --netuid 2`
- **Testnet:** `--subtensor.network test --netuid 118`
- **Staging/Localnet:** `--localnet`

## Code Architecture

### Overview

This is Subnet 2 of the Bittensor network - a decentralized AI network implementing Proof-of-Inference using zero-knowledge machine learning (zk-ML). The subnet rewards miners for generating verifiable AI predictions and validators for verifying these predictions.

### High-Level Architecture

```
neurons/
├── miner.py                 # Entry point for miners
├── validator.py             # Entry point for validators
├── cli_parser.py            # Command-line argument parsing
├── constants.py             # Global constants and configuration
├── protocol.py              # Protocol definitions (synapses)
├── execution_layer/         # Zero-knowledge proof execution
│   ├── circuit.py           # Circuit execution logic
│   ├── proof_handlers/      # ZK proof handlers (ezkl, circom, jolt)
│   └── verified_model_session.py  # Model inference sessions
├── deployment_layer/        # Circuit deployment and storage
│   └── circuit_store.py     # Circuit management
├── _miner/                  # Miner-specific code
│   ├── miner_session.py     # Main miner session loop
│   └── circuit_manager.py   # Miner circuit management
├── _validator/              # Validator-specific code
│   ├── core/                # Core validator functionality
│   │   ├── validator_loop.py    # Main validator loop
│   │   ├── request_pipeline.py  # Request processing pipeline
│   │   └── response_processor.py # Response handling
│   ├── api/                 # External API (FastAPI)
│   ├── competitions/        # Competition logic
│   ├── scoring/             # Scoring and weights
│   └── models/              # Data models
└── utils/                   # Shared utilities
```

### Execution Flow

**Miner:**
1. `miner.py` initializes config and creates `MinerSession`
2. `MinerSession` starts axon server for incoming requests
3. Handles queries through attached forward functions:
   - `queryZkProof`: Main inference requests
   - `handle_pow_request`: Proof-of-weights requests
   - Other request types
4. Uses `execution_layer` to run circuits and generate proofs
5. Returns proof + inference result to validator

**Validator:**
1. `validator.py` initializes config and creates `ValidatorSession`
2. `ValidatorSession` creates `ValidatorLoop`
3. `ValidatorLoop` orchestrates:
   - Querying miners via `RequestPipeline`
   - Processing responses via `ResponseProcessor`
   - Scoring via `ScoreManager`
   - Weight updates via `WeightsManager`
   - Competition evaluation
4. External API serves on port 8443 (configurable)

### Key Components

- **Execution Layer:** Handles zero-knowledge proof generation and verification using multiple backends (EZKL, Circom, Jolt)
- **Circuit Store:** Manages deployed circuit files from `deployment_layer/`
- **Request Pipeline:** Validates and processes incoming requests
- **Scoring System:** Tracks miner performance based on proof size, response time, etc.
- **Proof of Weights:** On-chain weight posting mechanism
- **Competitions:** Time-limited challenges for miners

### Configuration

Key configuration via `constants.py`:
- `DEFAULT_NETUID = 2` (mainnet)
- `VALIDATOR_REQUEST_TIMEOUT_SECONDS = 120`
- `CIRCUIT_TIMEOUT_SECONDS = 60`
- `MAX_CONCURRENT_REQUESTS = 16`
- Model IDs for proof-of-weights circuits
- Competition settings

### External Dependencies

- **EZKL:** Zero-knowledge proof system
- **SnarkJS:** JavaScript zk-SNARK toolkit
- **ONNX Runtime:** Neural network inference
- **PyTorch:** Deep learning framework
- **Bittensor:** Blockchain networking layer

### Data Flow

1. Validators query miners with input data
2. Miners process through deployed circuits
3. ZK proofs generated for verification
4. Results returned with proofs
5. Validators verify proofs and score responses
6. Scores used for weight updates
7. Weights posted on-chain periodically

## Key Development Notes

- **Package structure:** All code is in `neurons/` directory (see `pyproject.toml` setuptools config)
- **No tests directory:** Testing appears to be done manually or in external repos
- **Docker:** Primary deployment method; see `Dockerfile`
- **Circuit files:** Stored in `deployment_layer/` subdirectories by model hash
- **Pre-flight checks:** Automatic dependency installation on first run
- **Auto-update:** Enabled by default (disable with `--no-auto-update`)
- **Logging:** Bittensor logging with WandB integration option
- **Prometheus:** Optional metrics endpoint (port 9090)

## Important Files

- `neurons/constants.py`: Network and protocol constants
- `neurons/protocol.py`: Synapse definitions for Bittensor communication
- `neurons/_validator/core/validator_loop.py`: Main validator orchestration
- `neurons/_miner/miner_session.py`: Main miner orchestration
- `neurons/execution_layer/circuit.py`: Circuit execution logic
- `makefile`: All development and deployment commands
- `pyproject.toml`: Python configuration and dependencies
- `Dockerfile`: Container build configuration