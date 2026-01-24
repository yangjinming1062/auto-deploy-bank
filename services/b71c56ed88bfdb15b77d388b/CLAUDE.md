# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OurTube is a decentralized YouTube clone built on the Polygon network. Users can connect their wallet, upload videos to Livepeer/IPFS, and browse videos indexed by The Graph.

## Commands

```bash
# Frontend
npm run dev      # Start development server on localhost:3000
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint

# Smart contracts (root directory)
npx hardhat compile    # Compile Solidity contracts to artifacts/

# Subgraph (indexer)
cd indexer
yarn codegen           # Generate TypeScript types from GraphQL schema
yarn build             # Build the subgraph
yarn deploy            # Deploy to The Graph hosted service
yarn test              # Run subgraph tests
```

## Architecture

### Data Flow
1. **Upload Flow**: Video file → Livepeer | Thumbnail → IPFS (Web3.Storage) → Contract `uploadVideo()` call
2. **Query Flow**: The Graph indexes `VideoUploaded` events → GraphQL queries via Apollo Client

### Key Files
- **Smart Contract**: `contracts/OurTube.sol` - stores video metadata on-chain (hash, title, description, author)
- **Subgraph**: `indexer/src/ourtube.ts` - maps `VideoUploaded` events to GraphQL entities
- **Pages**: Next.js 12 pages using file-based routing
  - `/` - Landing page with wallet connect
  - `/home` - Video grid
  - `/upload` - Video upload form
  - `/video/[id]` - Video player page
- **Queries**: `queries/index.ts` - GraphQL queries for fetching videos
- **Clients**: `clients/apollo.ts` (The Graph), `clients/livepeer.ts` (video playback)
- **Constants**: `constants/index.ts` - contract address, subgraph URL, IPFS gateway

### Blockchain Configuration
- **Network**: Polygon Mumbai testnet
- **Contract**: `0xEd2e212B8191827cd27DcB60A09BA5F789eD78e2`
- **Subgraph**: `suhailkakar/ourtube-v2` on The Graph hosted service

### Tech Stack
- Next.js 12, React 18, TypeScript
- Ethers.js 5, Wagmi 0.6, RainbowKit 0.6
- Apollo Client 3 for GraphQL
- Hardhat 2, Solidity 0.8.9
- TailwindCSS 3, dark mode support via ThemeContext