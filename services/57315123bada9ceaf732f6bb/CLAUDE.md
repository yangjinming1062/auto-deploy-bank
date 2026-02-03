# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RankSys is a Java 8 framework for implementing and evaluating recommendation algorithms, with a particular focus on novelty and diversity for ranking tasks. The framework targets the **ranking task** (generating sorted recommendation lists) rather than rating prediction. This philosophy is reflected throughout the core interfaces and components.

## Build Commands

```bash
# Build the entire project
mvn clean install

# Run tests
mvn test

# Run a single test class
mvn test -Dtest=MFRecommenderTest -pl RankSys-mf

# Run a single test method
mvn test -Dtest=MFRecommenderTest#testRecommender -pl RankSys-mf

# Build a specific module (from root directory)
mvn install -pl RankSys-core -am
```

**Requirement**: Java 8 (1.8) must be available on the system.

## Architecture

RankSys is organized as a multi-module Maven project with 14 modules:

### Core Infrastructure
- **RankSys-core**: Base interfaces (`UserIndex`, `ItemIndex`, `PreferenceData`) and utility classes
- **RankSys-fast**: Performance-optimized implementations using `fastutil` data structures
- **RankSys-formats**: Readers/writers for various data formats
- **RankSys-compression**: In-memory compression techniques

### Recommendation Engine
- **RankSys-rec**: Core interfaces for `Recommender` and `Recommendation` generation
- **RankSys-nn**: Nearest neighbors algorithms (user-based and item-based)
- **RankSys-mf**: Matrix factorization techniques (ALS, implicit feedback, PLSA)
- **RankSys-lda**: Latent Dirichlet Allocation using Mallet
- **RankSys-fm**: Factorization Machines using JavaFM

### Evaluation & Metrics
- **RankSys-metrics**: Framework for defining `RecommendationMetric` and `SystemMetric`
- **RankSys-novelty**: Novelty metrics (long-tail, unexpectedness)
- **RankSys-diversity**: Diversity metrics (intent-aware, distance-based)
- **RankSys-novdiv**: Shared resources for novelty and diversity

### Examples
- **RankSys-examples**: Runnable examples demonstrating framework usage

## Key Design Patterns

### Core Interfaces
The framework uses generic types for flexibility with different ID types (typically `Long`):
- `UserIndex<U>` / `ItemIndex<I>`: Map between user/item IDs and internal integer indices
- `PreferenceData<U, I>`: Access to user-item preferences
- `Recommender<U, I>`: Generate ranked recommendation lists
- `Recommendation<U, I>`: A single user's recommendation list

### Fast Indexing
`FastItemIndex` and `FastUserIndex` extend core interfaces with integer-based lookups for performance. Use `SimpleFastUserIndex.load()` and `SimpleFastItemIndex.load()` to load pre-built indices.

### Metrics Composition
Metrics use a composable design:
- `RelevanceModel`: Determines relevance of items to users
- `DiscountModel`: Applies position-based discounts to ranking metrics
- Combine them in metrics like `NDCG`, `Precision`, `Recall`, `AlphaNDCG`

## Common Entry Points for Extension

- **Adding a new recommender**: Implement `Recommender<U, I>` interface
- **Adding a new metric**: Extend `RecommendationMetric` or `SystemMetric`
- **Adding a new similarity**: Create implementations in appropriate nn module
- **New data format support**: Implement readers in RankSys-formats

## Code Style

- Uses Java 8 features extensively (lambdas, `Stream` API, `Optional`)
- `java.util.logging.Logger` for internal diagnostics
- jOOL (`org.jooq.lambda`) for advanced functional operations on tuples

## Data Format Readers

Standard format readers (from `RankSys-formats`):
- `SimpleRatingPreferencesReader`: User-Item-Rating format
- `SimpleFeaturesReader`: Item-Feature-Value format
- `SimpleRecommendationFormat`: Input/output of recommendation lists

## License

MPL 2.0 - See LICENSE file for details.