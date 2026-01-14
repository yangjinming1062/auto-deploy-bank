# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Self is a monorepo for an identity wallet that generates privacy-preserving proofs from government-issued IDs (passports, ID cards, Aadhaar) using NFC scanning and zk-SNARKs. Key use cases include airdrop protection, humanity checks, and compliance verification.

## Common Development Commands

### Root Workspace Commands (run from repository root)
```bash
# Install dependencies
yarn install

# Build all packages (parallel, topological)
yarn build

# Run all tests across workspaces
yarn test

# Lint all packages
yarn lint

# Format code (root + all workspaces)
yarn format

# Type check all packages
yarn types

# Development setup for mobile app
yarn reinstall-app

# Mobile development
yarn demo:mobile  # Build SDK + demo and start
```

### Mobile App (app/)
```bash
cd app

# Platform-specific builds
yarn ios
yarn android

# Clean build
yarn clean
yarn setup  # Full setup with dependencies

# Testing
yarn test              # Jest tests + CJS test scripts
yarn test:coverage     # Coverage report
yarn test:e2e:ios      # iOS E2E with Maestro
yarn test:e2e:android  # Android E2E with Maestro
yarn test:build        # Build deps + types + bundle analysis + tests

# Web builds
yarn web               # Start Vite dev server
yarn web:build         # Production build
yarn web:preview       # Preview production build

# Code quality
yarn lint
yarn lint:fix
yarn fmt
yarn fmt:fix
```

### Circuits (circuits/)
```bash
cd circuits

# Build TypeScript dependencies
yarn build:deps

# Build circuits (requires circom)
./scripts/build_circuits.sh

# Run tests with sample data
yarn test
```

### Contracts (contracts/)
```bash
cd contracts

# Build contracts
yarn run build

# Deploy to Celo network
yarn run deploy:allverifiers:celo
yarn run deploy:registry:celo
yarn run deploy:hub:celo

# Testing with coverage
yarn run test:coverage:local
```

### Single Test Execution

#### Mobile App (React Native)
```bash
# Run specific test file
yarn test src/utils/someUtility.test.ts

# Run tests matching pattern
yarn test -t "testNamePattern"

# Run tests in watch mode
yarn test --watch
```

#### Other Packages
```bash
# For any workspace, run package-specific tests
yarn workspace @selfxyz/<package-name> test
```

## Architecture Overview

### Monorepo Structure

```
/
├── app/                      # React Native mobile app + web
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── screens/          # Feature-based screen components
│   │   ├── navigation/       # React Navigation config
│   │   ├── hooks/            # Custom React hooks
│   │   ├── stores/           # Zustand state management
│   │   ├── utils/            # Utilities (MRZ, proving, crypto, etc.)
│   │   ├── types/            # TypeScript definitions
│   │   └── providers/        # Context providers
│   ├── tests/                # Test files mirroring src/
│   └── android/ios/          # Native platforms
│
├── circuits/                 # zk-SNARK circuits (Circom)
│   ├── circuits/
│   │   ├── register/         # Identity registration circuits
│   │   └── disclose/         # Proof generation circuits
│   └── scripts/
│
├── contracts/                # Solidity smart contracts
│   ├── contracts/
│   │   ├── abstract/         # Abstract contracts
│   │   ├── interfaces/       # Contract interfaces
│   │   ├── libraries/        # Utility libraries
│   │   └── example/          # Integration examples
│   └── ignition/             # Hardhat Ignition deployments
│
├── common/                   # Shared utilities and data
│   ├── src/                  # Common code
│   ├── pubkeys/              # Public keys for countries
│   └── sanctionedCountries/  # Sanctioned country lists
│
├── sdk/                      # SDK implementations
│   ├── core/                 # Core SDK
│   ├── qrcode/               # QR code SDK
│   ├── qrcode-angular/       # Angular-specific QR SDK
│   └── sdk-go/               # Go SDK
│
└── packages/
    ├── mobile-sdk-alpha/     # Mobile SDK being migrated from app
    └── mobile-sdk-demo/      # SDK demonstration app
```

### Core Workflow Architecture

#### 1. Identity Verification Flow (Mobile App)
```
NFC Scan → MRZ Parsing → Certificate Chain Verification →
zk-Proof Generation → On-Chain Verification
```

**Key components:**
- **NFC Module**: Platform-specific (Swift iOS, Kotlin Android) wrapped in JavaScript interface
- **MRZ Processing**: `app/src/utils/` - Parses passport Machine Readable Zone
- **Validation**: Certificate chain and signature verification
- **Proving**: Zero-knowledge proof generation (circuit mode: offChain/onChain/register)
- **Storage**: AsyncStorage (simple), SQLite (proof history), Keychain (sensitive)

#### 2. Circuit Design (circuits/)
Circuits use `selector_mode` bitmap to control disclosure:

| Mode | selector_mode[0] | selector_mode[1] | Disclosed Attributes |
|------|------------------|------------------|---------------------|
| offChain | 1 | 1 | packedReveal-dg1, age, OFAC, country, pubKey |
| onChain | 1 | 0 | packedReveal-dg1, age, OFAC, country, blinded DSC |
| register | 0 | 0 | blinded DSC commitment, commitment |

**Supported signature algorithms:**
- ✓ sha256WithRSAEncryption, sha1WithRSAEncryption, sha256WithRSASSAPSS
- 🚧 ecdsa-with-SHA* variants (under development)

#### 3. Smart Contract Architecture (contracts/)
```
IdentityVerificationHub
├── IdentityRegistry (Passport + ID Card registries)
├── Document Signer Certificate (DSC) Verifiers
├── Proof Verifiers (Register, Disclose, VC)
├── OFAC Compliance System (3-tier validation)
└── Poseidon Hashing
```

**Key contracts:**
- `IdentityVerificationHubImplV2`: Main verification orchestrator
- `IdentityRegistryImplV1`: Manages identity commitments and nullifiers
- `SelfVerificationRoot`: Base contract for integrations

### Data Flow & Storage

#### Mobile App Persistence
- **AsyncStorage**: Simple key-value pairs
- **SQLite**: Proof history, protocol trees (complex queries)
- **Keychain**: Biometric data, encryption keys (sensitive)

#### Proof Generation Modes
1. **offChain**: Full proof with pubKey revealed
2. **onChain**: Proof without pubKey (uses blinded DSC commitment)
3. **register**: Identity commitment generation

### Platform-Specific Implementation

#### iOS
- Native module: `PassportReader` (Swift)
- Authentication: MRZ Key, PACE, BAC fallback
- Deployment: Fastlane

#### Android
- Native module: `RNPassportReaderModule` (Kotlin)
- Same authentication methods
- Deployment: Fastlane

#### Web
- Vite-based build
- Browser-compatible crypto adapters
- Same proving logic as mobile

## Testing Architecture

### Mobile App Testing (Jest)
- **Setup**: `jest.config.cjs` + `jest.setup.js` with comprehensive mocks
- **Module mapping**: `@/` → `src/`, `@tests/` → `tests/src/`
- **Mocks**: Firebase, Keychain, NFC, Analytics, native modules
- **Test types**: Unit (`.test.ts`), Integration (`.integration.test.ts`), E2E (Maestro YAML)

### SDK Testing (Vitest)
- **Location**: `packages/mobile-sdk-alpha/tests/`
- **Config**: `vitest.config.ts` with Node environment
- **Console**: Suppressed noise in `tests/setup.ts`

### Circuit Testing
- **Tool**: Circom + snarkjs
- **Coverage**: Build specific circuits for testing

### Contract Testing
- **Framework**: Hardhat + Mocha/Chai
- **Coverage**: Local coverage reports with circuit integration

## Key Development Patterns

### Navigation (React Native)
```typescript
// Static navigation with type safety
const navigationScreens = {
  ...systemScreens,
  ...passportScreens,
  ...homeScreens,
  // ...
};

initialRouteName: Platform.OS === 'web' ? 'Home' : 'Splash'
```

### State Management
- **Global**: Zustand stores
- **Local**: React hooks
- **Custom hooks**: `useModal`, `useHapticNavigation`
- **Providers**: Context-based dependencies

### Error Handling Pattern
```typescript
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  console.error('Operation failed:', error);
  return fallbackValue;
}
```

### Platform Detection
```typescript
if (Platform.OS === 'ios') {
  // iOS-specific implementation
} else {
  // Android-specific implementation
}
```

### Native Module Initialization
```typescript
const modulesReady = await initializeNativeModules();
if (!modulesReady) {
  console.warn('Native modules not ready, proceeding with limited functionality');
}
```

### Modal System
```typescript
const { showModal, dismissModal, visible } = useModal({
  titleText: 'Modal Title',
  buttonText: 'Action',
  onButtonPress: async () => { /* ... */ },
});
```

## Security & Privacy Requirements

### Critical Security Rules
- **NEVER log sensitive data**: No PII, credentials, tokens, API keys, private keys, or session identifiers
- **Always redact**: Use patterns like `***-***-1234` for passport numbers, `J*** D***` for names
- **Secure storage**: Keychain for sensitive, SQLite for complex, AsyncStorage for simple
- **Certificate validation**: Validate all passport certificates
- **Zero-knowledge proofs**: Ensure privacy-preserving verification at all times

### Privacy Features
- Selective attribute revelation (only disclose minimum necessary)
- Privacy-preserving age verification (without revealing DOB)
- Identity commitment privacy (commitments don't reveal identity)
- OFAC compliance without name exposure (Merkle tree verification)

## Migration: Mobile SDK Alpha

Current effort to migrate identity verification logic from `app/src/utils/` to `packages/mobile-sdk-alpha/` for partner SDK consumption.

**Key migration items:**
1. MRZ processing helpers → `packages/mobile-sdk-alpha/src/processing/`
2. Validation module → `packages/mobile-sdk-alpha/src/validation/`
3. Proof input generation → `packages/mobile-sdk-alpha/src/proving/`
4. Crypto adapters → `packages/mobile-sdk-alpha/src/crypto/`
5. TEE session management → `packages/mobile-sdk-alpha/src/tee/`

**Validation workflow:**
1. Create tests in mobile-sdk-alpha BEFORE migrating logic
2. Run `yarn test:build` in both `app/` and `packages/mobile-sdk-alpha/`
3. Incrementally migrate one item at a time
4. Update app imports to consume SDK

## Build System Requirements

### System Dependencies (for full build)
- **Node.js**: v22.x (use `.nvmrc`)
- **Yarn**: v4.6.0
- **Rust**: Latest (for Circom)
- **Circom**: v2.1.9 (for circuits)
- **wget**: Required for contract deployment scripts

### Dependencies by Package
- **app/**: React Native 0.76.9, Tamagui, React Navigation, Firebase, Sentry
- **circuits/**: Circom, snarkjs
- **contracts/**: Hardhat, OpenZeppelin, Ethers
- **common/**: TypeScript utilities, country data

## Branching & Contribution

- **Base branch**: `staging` (PRs from other branches are automatically closed)
- **Workflow**: Create feature branch → PR to `staging` → Code review → Merge

## Useful File References

- **Development Patterns**: `docs/development-patterns.md` - React Native architecture, navigation, state management
- **Testing Guide**: `docs/testing-guide.md` - Jest, mock patterns, E2E testing
- **Cursor Rules**:
  - `.cursorrules` - Main development guidelines
  - `.cursor/rules/mobile-sdk-migration.mdc` - SDK migration strategy
- **Architecture Overview**: `.cursor/rules/compliance-verification.mdc` - Identity verification system architecture
- **Contract Integration**: `contracts/README.md` - Smart contract integration examples
- **Circuit Details**: `circuits/README.md` - zk-SNARK circuit architecture

## Integration Examples

See these repositories for integration examples:
- [HappyBirthday](https://github.com/selfxyz/happy-birthday): Age verification example
- [Airdrop](https://github.com/selfxyz/self/tree/main/contracts/contracts/example/Airdrop.sol): Token distribution protection