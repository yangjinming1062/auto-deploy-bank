# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**LibRec** is an open-source Java library for recommender systems implementing 70+ state-of-the-art recommendation algorithms for two classic tasks: **rating prediction** and **item ranking**.

- **Website:** http://www.librec.net
- **Version:** 1.4 (under development)
- **License:** GNU GPL v3
- **Language:** Java 1.7+

## Repository Structure

This repository contains the LibRec project with the following structure:

```
/home/ubuntu/deploy-projects/f210554da9657b7fc28d4424/
├── README.md               # Main project documentation (features, execution, code examples)
├── CHANGES.md              # Version history (v1.0 to v1.4)
├── LICENSE                 # GNU GPL v3 license
├── CONTACT.md              # Contact and support information
├── Team.md                 # Team member profiles (Chinese)
├── 团队招募.md              # Team recruitment announcement (Chinese)
└── librec/                 # Main project directory
    ├── src/                # Source code (111 Java files)
    │   ├── main/java/librec/
    │   │   ├── main/       # Entry points (LibRec.java, Demo.java)
    │   │   ├── intf/       # Interfaces & base classes
    │   │   ├── data/       # Data structures (SparseMatrix, etc.)
    │   │   ├── rating/     # 20 rating prediction algorithms
    │   │   ├── ranking/    # 18 item ranking algorithms
    │   │   ├── baseline/   # 8 baseline methods
    │   │   ├── ext/        # 7 extension algorithms
    │   │   ├── metric/     # Evaluation metrics
    │   │   └── util/       # Utilities
    │   └── main/resources/ # Configuration & logging
    ├── demo/               # Demo configurations & datasets
    │   ├── config/         # 22 algorithm configuration files
    │   └── Datasets/       # Sample datasets (FilmTrust)
    ├── target/             # Compiled artifacts (librec-1.4.jar)
    ├── pom.xml             # Maven build configuration
    └── CLAUDE.md           # Detailed development guidance for code operations
```

## Quick Start for Development

### Build Commands
```bash
# Build the project (from librec directory)
cd librec
mvn clean package

# Run an algorithm with demo config
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf

# Run with parameter overrides
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf -D num.factors=50

# For large datasets, increase JVM heap
java -Xmx4g -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf
```

### Testing Approach
**No formal unit test suite exists.** Testing is done via:
- Demo configuration files in `librec/demo/config/`
- Sample dataset in `librec/demo/Datasets/FilmTrust/`
- Running algorithms and validating output in `./Results/`

**Note:** Always rebuild with `mvn clean compile` after making code changes.

## Key Documentation

### For All Users
- **README.md** - Main project documentation with features, examples, and code snippets
- **CONTACT.md** - Support, bug reporting, and contact information

### For Developers Working on Code
- **librec/CLAUDE.md** - Comprehensive guide for code operations including:
  - Detailed build and run commands
  - High-level architecture (6 main components)
  - Interface hierarchy and design patterns
  - Configuration system
  - Algorithm implementation patterns
  - Troubleshooting guide

### For Historical Context
- **CHANGES.md** - Detailed version history with features added in each version
- **Team.md** - Core team member profiles (Chinese)
- **团队招募.md** - Team recruitment information (Chinese)

## Project Architecture

LibRec follows a **modular, interface-based architecture** with six main components:

1. **Data Split** - Train/test splitting utilities
2. **Data Conversion** - Format conversion and normalization
3. **Similarity** - User/item similarity computation
4. **Algorithms** - 70+ recommendation algorithms
5. **Evaluators** - Performance metrics (MAE, RMSE, Precision, Recall, NDCG, etc.)
6. **Filters** - Result filtering and post-processing

### Algorithm Categories
- **Rating Prediction** (20 algorithms): PMF, BiasedMF, SVD++, UserKNN, TrustSVD, etc.
- **Item Ranking** (18 algorithms): BPR, WBPR, GBPR, WRMF, CLiMF, etc.
- **Baselines** (8 methods): GlobalAverage, MostPopular, UserCluster, etc.
- **Extensions** (7 methods): NMF, SlopeOne, LDA, etc.

### Core Design Pattern
All algorithms implement the `Recommender` interface with specialized extensions:
- `IterativeRecommender` - For iterative optimization (BPR, PMF, SVD++)
- `GraphicRecommender` - For probabilistic models (LDA, BUCM)
- `SocialRecommender` - For social-aware methods (TrustSVD, SocialMF)
- `TensorRecommender` - For tensor factorization
- `ContextRecommender` - For context-aware methods

## Common Development Tasks

### Running Different Algorithms
```bash
cd librec

# Bayesian Personalized Ranking
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf

# Matrix Factorization (Probabilistic)
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/PMF.conf

# Social Recommendation
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/TrustSVD.conf

# User-based Collaborative Filtering
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/UserKNN.conf
```

### Using Custom Datasets
1. Prepare dataset as tab/comma-separated file: `user-id, item-id, rating`
2. Create/edit configuration file (`.conf`) with dataset path:
   ```properties
   data.column.ratings=1,2,0
   data.input.path=/path/to/your/dataset.txt
   ```
3. Configure data format via `ratings.setup` parameter
4. Run: `java -cp target/librec-1.4.jar librec.main.LibRec -c your-config.conf`

### Adding New Algorithms
1. Extend appropriate base class in `librec/src/main/java/librec/`
2. Implement required methods: `setup()`, `trainModel()`, `predict()`
3. Add to configuration via `rec.recommender.class=YourClass`
4. Create demo config in `librec/demo/config/YourClass.conf`

**Detailed implementation patterns and examples available in: librec/CLAUDE.md**

## Configuration System

### Main Configuration
- **File:** `librec/src/main/resources/librec.conf`
- **Sections:**
  - Essential Setup (dataset paths, algorithm, evaluation)
  - Model-based Methods (factors, iterations, learning rate)
  - Memory-based Methods (similarity metrics, neighbors)
  - Method-specific Settings (per-algorithm parameters)

### Demo Configurations
- **Directory:** `librec/demo/config/`
- **Contains:** 22 ready-to-use configuration files for various algorithms
- **Examples:** BPR.conf, PMF.conf, UserKNN.conf, TrustSVD.conf, WRMF.conf, etc.

### Runtime Override
Override config values via command-line:
```bash
java -cp target/librec-1.4.jar librec.main.LibRec \
  -c demo/config/BPR.conf \
  -D rec.recommender.class=BPR \
  -D num.factors=100 \
  -D rec.iterator.maximum=50
```

## Dependencies & Build System

- **Build System:** Apache Maven 3.x
- **Java Version:** 1.7 (source/target compatibility)
- **Key Dependencies:**
  - `slf4j-log4j12` 1.7.21 (logging)
  - `javax.mail` 1.4.5 (email notifications)
  - `guava` 16.0 (Google utilities)

**Build Commands:**
```bash
cd librec
mvn clean compile      # Compile only
mvn clean package      # Build JAR
mvn clean install      # Install to local repository
```

## Key Files to Know

### Entry Points
- `librec/src/main/java/librec/main/LibRec.java` (908 lines) - Main command-line interface
- `librec/src/main/java/librec/main/Demo.java` (208 lines) - Demo runner

### Core Interfaces
- `librec/src/main/java/librec/intf/Recommender.java` - Base interface for all algorithms
- `librec/src/main/java/librec/intf/IterativeRecommender.java` - Base for iterative methods

### Data Structures
- `librec/src/main/java/librec/data/SparseMatrix.java` - Core sparse matrix implementation
- `librec/src/main/java/librec/data/DataDAO.java` - Data loading utilities

### Configuration & Logging
- `librec/src/main/resources/librec.conf` - Default configuration template
- `librec/src/main/resources/log4j.xml` - Logging configuration

## Troubleshooting

**"NoSuchMethodError" after code changes**
- **Solution:** Run `mvn clean compile` to rebuild classes

**Results not appearing in ./Results/**
- **Solution:** Check `output.setup` path in config is correct and writable

**OutOfMemoryError during training**
- **Solution:** Increase JVM heap: `java -Xmx4g -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf`

**"ClassNotFoundException"**
- **Solution:** Rebuild JAR: `mvn clean package`

**Algorithm not loading**
- **Solution:** Verify `rec.recommender.class` matches algorithm class name

**For more troubleshooting, see: librec/CLAUDE.md**

## Programmatic API Usage

LibRec can be integrated into Java applications:

```java
// 1. Configuration
Configuration conf = new Configuration();
Resource resource = new Resource("rec/cf/userknn-test.properties");
conf.addResource(resource);

// 2. Data model
DataModel dataModel = new TextDataModel(conf);
dataModel.buildDataModel();

// 3. Context
RecommenderContext context = new RecommenderContext(conf, dataModel);
RecommenderSimilarity similarity = new PCCSimilarity();
similarity.buildSimilarityMatrix(dataModel, true);
context.setSimilarity(similarity);

// 4. Training
Recommender recommender = new UserKNNRecommender();
recommender.recommend(context);

// 5. Evaluation
RecommenderEvaluator evaluator = new MAEEvaluator();
recommender.evaluate(evaluator);
```

**For complete API examples, see README.md**

## Research & Academic Context

**Citing LibRec:**
If LibRec is helpful to your research, please cite:
1. Guibing Guo, Jie Zhang, Zhu Sun and Neil Yorke-Smith, "LibRec: A Java Library for Recommender Systems", UMAP, 2015.
2. G. Guo, J. Zhang and N. Yorke-Smith, "TrustSVD: Collaborative Filtering with Both the Explicit and Implicit Influence of User Trust and of Item Ratings", AAAI, 2015.

**Publications Using LibRec:**
- TrustSVD (AAAI 2015) - Collaborative filtering with trust
- Implicit Item Relationships (UMAP 2015) - Exploiting item relationships

**Contributors:**
Prof. Robin Burke, Bin Wu, Ge Zhou, Ran Locar, Shawn Rutledge, Tao Lian, Takuya Kitazawa, and others.

## Version Information

- **Current Version:** 1.4 (under development)
- **Previous Releases:** 1.3, 1.2, 1.1, 1.0
- **Future Plans:** README mentions LibRec 2.0 aspirationally
- **Version History:** See CHANGES.md for detailed changelog

## Support & Community

- **Website:** http://www.librec.net
- **Gitter Chat:** https://gitter.im/librec/Lobby
- **WeChat:** Official WeChat group for updates (QR code in README.md)
- **Bug Reports:** See CONTACT.md for issue reporting guidelines

## Important Notes

- The codebase is self-contained - all utilities merged into `librec.util` package
- Results are written to `./Results/` with timestamped filenames
- Static context pattern used - remember to reset between multiple runs
- No CI/CD pipeline - manual build and release process
- No formal unit test suite - testing via demo configurations

## For More Details

**Code-specific guidance, architecture details, and implementation patterns:** See `librec/CLAUDE.md`

This file provides high-level repository guidance. The detailed development guide in `librec/CLAUDE.md` contains comprehensive information about code structure, algorithms, and development workflows.