# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Build & Run
```bash
# Build the project
mvn clean package

# Run algorithm with demo config
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf

# Run with command-line overrides
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf -D rec.recommender.class=BPR -D num.factors=50

# Alternative: use librec wrapper command (requires librec CLI tool installed)
librec rec -exec -conf demo/config/BPR.conf
librec rec -exec -D rec.recommender.class=BPR -D num.factors=50

# Print version
java -cp target/librec-1.4.jar librec.main.LibRec -v
```

### Development Workflow
1. Edit Java source files in `src/main/java/librec/`
2. Build: `mvn clean compile`
3. Run: `java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf`
4. View results in `./Results/` directory

### Testing & Linting
**No formal unit test suite exists.** Testing is done via:
- Demo configuration files in `demo/config/`
- Sample dataset in `demo/Datasets/FilmTrust/`
- Running algorithms and validating output in `./Results/`

**Linting:** No automated linting tools configured. Code follows standard Java conventions.

### Memory Optimization
```bash
# For large datasets, increase JVM heap
java -Xmx4g -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf
```

## Project Overview

**LibRec v1.4** is a Java library for recommender systems implementing **70+ recommendation algorithms** for:
- **Rating Prediction** (20 algorithms): PMF, BiasedMF, SVD++, UserKNN, TrustSVD, etc.
- **Item Ranking** (18 algorithms): BPR, WBPR, GBPR, WRMF, CLiMF, etc.
- **Baselines** (8 methods): GlobalAverage, MostPopular, UserCluster, etc.
- **Extensions** (7 methods): NMF, SlopeOne, LDA, etc.

**Total:** 111 Java source files across 8 packages (baseline, rating, ranking, ext, data, intf, metric, util, main)

**Website:** http://www.librec.net  |  **License:** GNU GPL v3

## High-Level Architecture

### Six Main Components

LibRec consists of **six modular components**:

1. **Data Split** - Train/test splitting (`librec.data.DataSplitter`)
2. **Data Conversion** - Format conversion and normalization (`librec.data.DataDAO`)
3. **Similarity** - User/item similarity computation (`librec.intf.RecommenderSimilarity`)
4. **Algorithms** - Recommendation algorithms (`librec.rating.*`, `librec.ranking.*`)
5. **Evaluators** - Performance metrics computation (`librec.metric.*`)
6. **Filters** - Result filtering (`librec.util.RecommendedFilter`)

### Core Framework Design

The framework uses an **interface-based architecture** where all algorithms implement the `Recommender` interface:

```
librec.intf.Recommender (base interface)
├── IterativeRecommender (for iterative optimization: BPR, PMF, SVD++)
│   └── extends Recommender
├── GraphicRecommender (for probabilistic models: LDA, BUCM)
│   └── extends Recommender
├── SocialRecommender (for social-aware: TrustSVD, SocialMF)
│   └── extends Recommender
├── TensorRecommender (for tensor factorization)
│   └── extends Recommender
└── ContextRecommender (for context-aware methods)
    └── extends Recommender
```

### Key Components by Package

**Data Layer (`data/` - 22 files)**:
- `SparseMatrix.java` - Core sparse matrix structure (CRS/CCS implementations)
- `DenseMatrix.java`, `DenseVector.java` - Dense data structures
- `DataDAO.java` - Data loading from various file formats
- `DataSplitter.java` - Train/test split utilities
- `SparseTensor.java` - Tensor data structures
- `Configuration.java`, `Resource.java` - Configuration management

**Algorithm Layer**:
- `rating/` (20 algorithms) - Rating prediction algorithms
- `ranking/` (18 algorithms) - Item ranking algorithms
- `baseline/` (8 methods) - Baseline recommenders
- `ext/` (7 algorithms) - Specialized extensions

**Evaluation Layer (`metric/` - 10 files)**:
- `IRatingMetric.java` - MAE, RMSE, rMAE, rRMSE, MPE
- `IRankingMetric.java` - Precision, Recall, NDCG, MAP, etc.
- `ITimeMetric.java` - Time-aware metrics
- `MetricCollection.java` - Metric aggregation

**Entry Points**:
- `librec.main.LibRec.java` (908 lines) - Command-line interface
- `librec.main.Demo.java` (208 lines) - Demo runner

### Static Context Pattern

**Critical Design Pattern:** The framework uses **static fields on `Recommender`** for global context:

```java
public abstract class Recommender {
    // Static global context (available to all algorithms)
    protected static Configuration cf;          // Current configuration
    protected static SparseMatrix rateMatrix;   // Training data matrix
    protected static SparseMatrix timeMatrix;   // Timestamps
    protected static DataDAO rateDao;           // Data access object
    protected static String tempDir;            // Output directory

    // Methods to access and manipulate context
    public static void resetStatics() { ... }   // Reset between runs
}
```

**⚠️ Important:** Set `Recommender.resetStatics()` to `true` between multiple runs to prevent state contamination across algorithm executions.

### Data Flow

```
Configuration (.conf) → FileConfiger → Configuration Object
         ↓
Dataset Files → DataDAO → SparseMatrix (rateMatrix, timeMatrix)
         ↓
DataSplitter → Train/Test Split
         ↓
Algorithm Class (via reflection) → Algorithm-specific Processing
         ↓
Evaluation Metrics (MAE, RMSE, Precision, etc.)
         ↓
Results → ./Results/ directory (timestamped files)
```

## Configuration System

### Main Configuration
**File:** `src/main/resources/librec.conf`

Contains 4 sections:
1. **Essential Setup** - Dataset paths, algorithm selection, evaluation setup
2. **Model-based Methods** - Matrix factorization parameters (num.factors, iterations, learning rate)
3. **Memory-based Methods** - CF parameters (similarity metrics, num.neighbors)
4. **Method-specific Settings** - Per-algorithm overrides

### Demo Configurations
**Directory:** `demo/config/` (22 ready-to-use examples)

Examples:
- `BPR.conf` - Bayesian Personalized Ranking
- `PMF.conf` - Probabilistic Matrix Factorization
- `UserKNN.conf`, `ItemKNN.conf` - Neighborhood-based CF
- `TrustSVD.conf` - Social-aware recommendation
- `WRMF.conf`, `CLiMF.conf` - Ranking-based MF

### Runtime Configuration Override
Override config values via command-line:
```bash
java -cp target/librec-1.4.jar librec.main.LibRec \
  -c demo/config/BPR.conf \
  -D rec.recommender.class=BPR \
  -D num.factors=100 \
  -D rec.iterator.maximum=50
```

## Programmatic API Usage

LibRec can be integrated into Java applications:

```java
import librec.data.*;
import librec.intf.*;
import librec.rating.*;

public void main(String[] args) throws Exception {
    // 1. Recommender configuration
    Configuration conf = new Configuration();
    Resource resource = new Resource("rec/cf/userknn-test.properties");
    conf.addResource(resource);

    // 2. Build data model
    DataModel dataModel = new TextDataModel(conf);
    dataModel.buildDataModel();

    // 3. Set recommendation context
    RecommenderContext context = new RecommenderContext(conf, dataModel);
    RecommenderSimilarity similarity = new PCCSimilarity(); // or COS, MSD
    similarity.buildSimilarityMatrix(dataModel, true);
    context.setSimilarity(similarity);

    // 4. Training
    Recommender recommender = new UserKNNRecommender();
    recommender.recommend(context);

    // 5. Evaluation
    RecommenderEvaluator evaluator = new MAEEvaluator(); // or RMSEEvaluator
    recommender.evaluate(evaluator);

    // 6. Get recommendation results
    List<RecommendedItem> recommendedItemList = recommender.getRecommendedList();
    RecommendedFilter filter = new GenericRecommendedFilter();
    recommendedItemList = filter.filter(recommendedItemList);
}
```

## Key Files & Locations

- **Build config:** `pom.xml` (Maven, Java 1.7, dependencies)
- **Default config:** `src/main/resources/librec.conf`
- **Main CLI:** `src/main/java/librec/main/LibRec.java`
- **Core interface:** `src/main/java/librec/intf/Recommender.java`
- **Sample dataset:** `demo/Datasets/FilmTrust/` (ratings.txt, trust.txt)
- **Logging config:** `src/main/resources/log4j.xml`

## Algorithm Selection Guide

### For Rating Prediction
- **Matrix Factorization:** PMF, BiasedMF, BPMF, SVD++, TimeSVD++
- **Memory-based:** UserKNN, ItemKNN
- **Social-aware:** TrustSVD, SocialMF, TrustMF, RSTE, SoRec, SoReg
- **Extensions:** LDCC, GPLSA, URP, CPTF

### For Item Ranking
- **Bayesian Personalized Ranking:** BPR, WBPR, GBPR, SBPR, AoBPR
- **Weighted Regularization:** WRMF, CLiMF
- **Similarity-based:** FISMauc, FISMrmse, SLIM
- **Topic Modeling:** LDA, BHfree, BUCM
- **Ranking-based MF:** RankALS, RankSGD

### Baselines
- **Averaging:** GlobalAverage, UserAverage, ItemAverage
- **Clustering:** UserCluster, ItemCluster
- **Popularity:** MostPopular
- **Random:** RandomGuess, ConstantGuess

## Implementation Guide

### Adding New Algorithms

1. **Extend appropriate base class:**
   ```java
   public class YourAlgorithm extends IterativeRecommender { ... }
   ```

2. **Implement required methods:**
   - `setup()` or `initModel()` - Initialize parameters
   - `trainModel()` - Training logic (for iterative methods)
   - `buildModel()` - Model building (for non-iterative methods)
   - `predict(int user, int item)` - Prediction logic

3. **Add to configuration:**
   ```properties
   rec.recommender.class=YourAlgorithm
   ```

4. **Create demo config:** `demo/config/YourAlgorithm.conf`

### Common Implementation Patterns

**Matrix Factorization (IterativeRecommender):**
```java
public class YourMF extends IterativeRecommender {
    protected double[][] P;  // User latent factors
    protected double[][] Q;  // Item latent factors

    @Override
    protected void initModel() throws Exception {
        P = new double[numUsers][numFactors];
        Q = new double[numItems][numFactors];
        // Initialize randomly or using strategies
    }

    @Override
    protected void trainModel() throws Exception {
        for (int iter = 1; iter <= numMaxIter; iter++) {
            // SGD/ALS training loop
            // Update P and Q based on gradients
        }
    }

    @Override
    protected double predict(int user, int item) {
        return denseMatrixMultipy(P[user], Q[item]);
    }
}
```

**Memory-based Collaborative Filtering (Recommender):**
```java
public class YourKNN extends Recommender {
    protected double[][] similarityMatrix;

    @Override
    protected void buildModel() throws Exception {
        similarityMatrix = new double[numUsers][numUsers];
        // Compute user-user or item-item similarity
        for (int u = 0; u < numUsers; u++) {
            for (int v = u + 1; v < numUsers; v++) {
                similarityMatrix[u][v] = computeSimilarity(u, v);
            }
        }
    }

    @Override
    protected double predict(int user, int item) {
        // Aggregate ratings from similar users/items
        double score = 0.0;
        double simSum = 0.0;

        for (int neighbor : getNeighbors(user, item)) {
            double sim = similarityMatrix[user][neighbor];
            double rating = rateMatrix.get(neighbor, item);
            score += sim * rating;
            simSum += Math.abs(sim);
        }

        return simSum > 0 ? score / simSum : globalMean;
    }
}
```

### Configuration-Driven Design

All algorithm parameters are loaded via the Configuration object:

```java
// Integer parameters
int numFactors = cf.getInt("num.factors", 50);
int numNeighbors = cf.getInt("num.neighbors", 20);

// Double parameters
double learningRate = cf.getDouble("learn.rate", 0.01);
double regL2 = cf.getDouble("reg.l2", 0.01);
double rho = cf.getDouble("rho", 0.5);

// Boolean parameters
boolean isVerbose = cf.getBoolean("rec.verbose", true);

// String parameters
String similarity = cf.get("rec.similarity.measure", "PCC");
```

## Common Development Tasks

### Running Different Algorithms
```bash
# Bayesian Personalized Ranking
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf

# User-based Collaborative Filtering
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/UserKNN.conf

# Matrix Factorization
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/PMF.conf

# Social Recommendation
java -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/TrustSVD.conf
```

### Using Custom Datasets

1. **Prepare dataset:** Create tab/comma-separated file with user-id, item-id, rating
2. **Configure dataset path:** Edit `.conf` file:
   ```properties
   data.column.ratings=1,2,0
   data.input.path=path/to/your/dataset.txt
   ```
3. **Set data format:** Configure `ratings.setup` parameter
4. **Run with config:** `java -cp target/librec-1.4.jar librec.main.LibRec -c your-config.conf`

### Cross-Validation
Enable k-fold cross-validation in config:
```properties
rec.evaluation.fold.cv=5
```

## Troubleshooting

**"NoSuchMethodError" after code changes**
- **Solution:** Run `mvn clean compile` to rebuild classes

**Results not appearing in ./Results/**
- **Solution:** Check `output.setup` path in config is correct and writable

**OutOfMemoryError during training**
- **Solution:** Increase JVM heap: `java -Xmx8g -cp target/librec-1.4.jar librec.main.LibRec -c demo/config/BPR.conf`

**"ClassNotFoundException"**
- **Solution:** Rebuild JAR: `mvn clean package`

**Algorithm not loading**
- **Solution:** Verify `rec.recommender.class` matches algorithm class name

**Static context contamination**
- **Solution:** Set `Recommender.resetStatics = true` between runs

**Incorrect similarity metrics**
- **Solution:** Check `rec.similarity.measure` parameter (PCC, COS, MSD, Jaccard, etc.)

## Version & Dependencies

- **Version:** 1.4 (under development; README mentions 2.0 aspirationally)
- **Java:** 1.7+ (source/target compatibility)
- **Build System:** Apache Maven 3.x
- **Dependencies:**
  - `slf4j-log4j12` 1.7.21 (logging facade)
  - `javax.mail` 1.4.5 (email notifications)
  - `guava` 16.0 (Google utilities)
- **License:** GNU General Public License v3

## Project Structure

```
librec/                                    # Maven project root
├── src/main/java/librec/
│   ├── main/                              # Entry points
│   │   ├── LibRec.java                    # Main CLI (908 lines)
│   │   └── Demo.java                      # Demo runner
│   ├── intf/                              # Interfaces & base classes
│   │   ├── Recommender.java               # Base interface
│   │   ├── IterativeRecommender.java      # Iterative methods
│   │   └── ... (7 interfaces total)
│   ├── data/                              # Data structures (22 files)
│   │   ├── SparseMatrix.java              # Core sparse matrix
│   │   ├── DataDAO.java                   # Data access layer
│   │   ├── DataSplitter.java              # Train/test splitting
│   │   └── ... (22 files)
│   ├── rating/                            # Rating prediction (20 algos)
│   │   ├── PMF.java
│   │   ├── SVDPlusPlus.java
│   │   ├── TrustSVD.java
│   │   └── ... (20 files)
│   ├── ranking/                           # Item ranking (18 algos)
│   │   ├── BPR.java
│   │   ├── WRMF.java
│   │   └── ... (18 files)
│   ├── baseline/                          # Baselines (8 methods)
│   ├── ext/                               # Extensions (7 methods)
│   ├── metric/                            # Evaluation (10 files)
│   │   ├── MAEEvaluator.java
│   │   ├── RMSEEvaluator.java
│   │   ├── PrecisionEvaluator.java
│   │   └── ... (10 files)
│   └── util/                              # Utilities (25 files)
│       ├── FileIO.java
│       ├── Logs.java
│       ├── Maths.java
│       └── ... (25 files)
├── src/main/resources/
│   ├── librec.conf                        # Default configuration
│   └── log4j.xml                          # Logging setup
├── demo/
│   ├── config/                            # 22 demo configurations
│   │   ├── BPR.conf
│   │   ├── PMF.conf
│   │   └── ... (22 configs)
│   └── Datasets/
│       └── FilmTrust/                     # Sample dataset
│           ├── ratings.txt
│           ├── trust.txt
│           └── readme.txt
├── target/
│   └── librec-1.4.jar                     # Compiled JAR
├── .settings/                             # Eclipse IDE settings
├── pom.xml                                # Maven configuration
└── .gitignore                             # Git ignore rules
```