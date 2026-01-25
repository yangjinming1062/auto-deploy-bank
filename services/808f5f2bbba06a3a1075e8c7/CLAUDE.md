# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

P2Rank is a ligand-binding site prediction tool based on machine learning. It predicts pockets on protein structures by scoring and clustering points on the solvent-accessible surface using a trained RandomForest classifier.

**Requirements:** Java 17-24, Gradle (included via wrapper)

## Build Commands

```bash
./make.sh                    # Build the project (runs gradle assemble)
./gradlew test              # Run unit tests
./unit-tests.sh             # Same as above
./tests.sh quick            # Fast test set for basic validation
./tests.sh all              # Comprehensive tests (requires external datasets from p2rank-datasets)
./gradlew dependencyUpdates # Check for dependency updates
```

**Run the program:**
```bash
distro/prank predict -f test_data/1fbl.pdb    # Production binary
./prank.sh help                               # Development mode
```

## Architecture

### Main Entry Point
- **`Main.groovy`** - Parses command-line arguments and dispatches to command handlers (`runPredict()`, `runRescore()`, etc.)
- **`P2Rank.groovy`** - Static helper methods for execution and shutdown

### Commands
Commands are defined in `Main.run()` as a switch statement. Key commands:
- `predict` / `eval-predict` - Predict ligand-binding sites (and evaluate against known ligands)
- `rescore` / `eval-rescore` - Rescore pockets from other methods (Fpocket, ConCavity, etc.)
- `fpocket-rescore` - Run Fpocket and rescore in one command
- `crossval` - Cross-validation for model training
- `eval` - Evaluate predictions against known ligands
- `analyze`, `transform`, `print`, `bench` - Utility commands

### Core Domain Model (`domain/`)
- **`Protein.groovy`** - Central class encapsulating protein structure, atoms, ligands, and computed surfaces
  - Computes solvent-accessible surface (SAS) from protein atoms
  - Manages ligand information and residue chains
- **`Residue.groovy`** - Amino acid residue with sequence info, secondary structure, and exposure status
- **`Pocket.groovy`** - Predicted ligand-binding pocket with scores and assigned residues
- **`Dataset.groovy`** - Collection of proteins/structures with processing logic
- **`Ligand.groovy`** - Ligand molecules extracted from PDB/mmCIF files

### Prediction Pipeline (`prediction/pockets/`)
- **`rescorers/ModelBasedRescorer.groovy`** - Main scoring engine that applies ML model to SAS points
  - Uses `FeatureExtractor` to compute features for each surface point
  - Clusters high-scoring points into pockets
- **`PocketPredictor.groovy`** - Finds and clusters SAS points to form pockets

### Feature Calculation (`features/`)
- **`FeatureExtractor.groovy`** - Interface for computing features on protein points
- **`PrankFeatureExtractor.groovy`** - Main implementation computing SAS point features
- Feature implementations in `implementation/`:
  - `chem/` - Chemical properties
  - `conservation/` - Conservation scores
  - `prop/` - Protrusion/solvent exposure
  - `secstruct/` - Secondary structure
  - `volsite/` - VolSite pharmacophore features

### Machine Learning (`program/ml/`)
- **`Model.groovy`** - Wraps Weka classifiers (RandomForest, FastRandomForest)
- Supports model formats: v1 (serialized Weka), v2 (.model2), v3 (directory with zstd-compressed classifier)

### Geometry (`geom/`)
- **`Atoms.groovy`** - Collection of atoms with spatial queries (KNN, within radius)
- **`Surface.groovy`** - Solvent-accessible surface computation via tessellation
- **`kdtree/`** - KD-tree implementation for efficient spatial queries
- **`Point.groovy`** - 3D point with distance calculations

### Configuration
- **`config/default.groovy`** - Default parameters
- **`config/default_rescore.groovy`** - Default rescoring parameters
- **`config/alphafold.groovy`** - Config for AlphaFold models
- **`src/main/groovy/cz/siret/prank/program/params/Params.groovy`** - All parameter definitions with documentation

### Testing
- Unit tests in `src/test/groovy/` using JUnit 5
- Tests require `distro/test_data/` and `distro/models/` directories
- Integration tests in `misc/test-scripts/`

### Key Workflow
1. Load protein structure (PDB/mmCIF/BinaryCIF)
2. Compute solvent-accessible surface (tessellated sphere points)
3. Calculate features for each surface point
4. Apply ML model to get ligandability scores
5. Cluster high-scoring points into pockets
6. Rank and output pockets with associated residues

## Style Notes

- Code uses Groovy `@CompileStatic` for performance
- Heavy use of closure-based processing (e.g., `dataset.processItems { }`)
- Logging via `@Slf4j` with log level control
- Parameters accessed via `Params.inst` or `@Parametrized` interface
- Spatial queries on `Atoms` use KD-tree for efficiency