# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Merkle Airdrop Starter - A monorepo for bootstrapping ERC20 token airdrops using Merkle trees. The system has three independent packages that work together:

1. **generator** - Generates Merkle tree root and proof data from recipient list
2. **contracts** - Solidity smart contract (ERC20 + MerkleClaim) for trustless claiming
3. **frontend** - Next.js web interface for users to connect wallets and claim tokens

## Commands

### Generator (generate Merkle tree data)
```bash
cd generator
npm install
# Edit config.json with recipient addresses and amounts
npm run start
# Outputs merkle.json with root and tree for contracts/frontend
```

### Contracts (Solidity with Foundry)
```bash
cd contracts
forge update  # Install dependencies
forge test    # Run tests
forge test -vvvv  # Run with stack traces
forge create  # Deploy contracts (see Foundry docs)
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev   # Development server
npm run build # Production build
npm run start # Start production server
npm run lint  # Run ESLint
```

## Architecture

### Data Flow
1. **Generator**: Reads `config.json` → Creates Merkle tree → Outputs `merkle.json`
2. **Contracts**: Deploy with Merkle root from generator → Users call `claim(address, amount, proof)`
3. **Frontend**: Loads `config.ts` (same data as generator) + `merkle.json` → User connects wallet → Generates proof client-side → Calls contract

### Key Integration Points
- `generator/config.json` and `frontend/config.ts` must have identical recipient lists and decimals
- Generator outputs `merkle.json` - copy `root` to contract deployment, `tree` to frontend public folder
- Frontend reads `NEXT_PUBLIC_CONTRACT_ADDRESS` from `.env.local`

### State Management (Frontend)
- Uses `unstated-next` for React state containers
- `state/eth.ts` - Wallet connection via Blocknative Onboard
- `state/token.ts` - Airdrop status, claim logic, Merkle proof generation

### Merkle Implementation
- **Leaf format**: `keccak256(address, amount)` - matching Solidity's `keccak256(abi.encodePacked(to, amount))`
- Tree options: `sortPairs: true` for deterministic proofs
- Leaf generation: `solidityKeccak256(["address", "uint256"], [address, value])`