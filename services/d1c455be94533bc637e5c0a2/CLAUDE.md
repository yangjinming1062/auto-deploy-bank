# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the Eclipse Deeplearning4J (DL4J) examples repository - a collection of standalone Maven projects demonstrating various features of the DL4J ecosystem for JVM-based deep learning applications. Each subdirectory contains an independent Maven project with its own `pom.xml`.

## Repository Structure

The repository contains multiple example projects:

- **dl4j-examples**: Core DL4J API examples (feedforward, CNN, RNN, autoencoders, VAE)
- **samediff-examples**: SameDiff API examples (graph-based automatic differentiation)
- **nd4j-ndarray-examples**: NDArray manipulation examples (similar to NumPy)
- **data-pipeline-examples**: DataVec ETL pipeline examples for data loading and preprocessing
- **dl4j-distributed-training-examples**: Distributed training on Apache Spark
- **tensorflow-keras-import-examples**: Importing Keras and TensorFlow models
- **onnx-import-examples**: ONNX model import examples
- **android-examples**: Android application using DL4J
- **mvn-project-template**: Clean project template for starting new projects
- **oreilly-book-dl4j-examples**: Historical examples (marked as outdated in README)

Each project follows the structure:
```
project-name/
├── pom.xml
├── README.md (describes examples and recommended exploration order)
└── src/
    ├── main/java/org/deeplearning4j/examples/...
    ├── main/resources/logback.xml
    └── test/java/... (minimal tests)
```

## Build System

**Maven** is the primary build tool. Each project has its own `pom.xml` with:
- Dependencies on DL4J ecosystem artifacts
- Maven compiler plugin (Java 8)
- Maven surefire plugin for testing
- Maven shade plugin for creating executable JARs with dependencies
- Exec-maven-plugin for running examples

### Common Commands

```bash
# Build a project (from project directory)
mvn clean package

# Run tests
mvn test

# Run a single test
mvn test -Dtest=QuickTest

# Run an example
mvn exec:java -Dexec.mainClass="org.deeplearning4j.examples.quickstart.modeling.feedforward.classification.IrisClassifier"

# Format code (Google Java style, 120-char wrap, 4-space indent)
mvn formatter:format

# Clean build artifacts
mvn clean
```

**Note**: Run commands from within the specific example project directory (where `pom.xml` is located).

## Code Architecture

### Example Organization

Examples are typically organized in two tiers:

1. **Quickstart**: Basic examples introducing core concepts
   - Feedforward networks (classification, regression, unsupervised)
   - Convolutional Neural Networks (LeNet, CIFAR)
   - Recurrent Neural Networks (UCI sequences, character modeling)
   - Variational Auto Encoders
   - Core features (model saving/loading, early stopping, UI)

2. **Advanced**: Complex use cases
   - Computer vision (YOLO, style transfer, captcha recognition)
   - NLP (text classification with word2vec, char modeling, embeddings)
   - Sequence modeling (anomaly detection)
   - Transfer learning
   - Custom layers, activations, loss functions

### Key Dependencies

Each project uses:
- `nd4j-backend` (nd4j-native or nd4j-cuda-X-platform for GPU)
- `deeplearning4j-core` - Core DL4J functionality
- `datavec-api` - Data loading and ETL
- `deeplearning4j-ui` - Training visualization
- JUnit Jupiter for testing
- Logback for logging

### Running Examples

**Method 1: Using Maven exec plugin**
```bash
cd dl4j-examples
mvn exec:java -Dexec.mainClass="org.deeplearning4j.examples.quickstart.modeling.feedforward.classification.IrisClassifier"
```

**Method 2: Using runexamples.sh (oreilly-book-dl4j-examples only)**
```bash
cd oreilly-book-dl4j-examples
./runexamples.sh --all
```

**Method 3: From built JAR**
```bash
cd dl4j-examples
mvn clean package
java -cp target/dl4j-examples-*-bin.jar org.deeplearning4j.examples.quickstart.modeling.feedforward.classification.IrisClassifier
```

## Development Guidelines

### Code Style

The repository follows **Google Java Style** with two modifications:
- 120-character column wrap
- 4-space indentation

Format code using:
```bash
mvn formatter:format
```

Eclipse formatter configuration may be available in `contrib/formatter.xml` at the repository root (if the contrib directory exists).

### Adding New Examples

1. Place new examples in appropriate directories:
   - `src/main/java/org/deeplearning4j/examples/quickstart/` for basic examples
   - `src/main/java/org/deeplearning4j/examples/advanced/` for complex examples
2. Follow naming conventions (typically ending with the example type, e.g., `IrisClassifier.java`)
3. Include comprehensive comments explaining the concepts
4. Reference relevant publications in code comments when applicable
5. Add a test in `src/test/java/` if fixing bugs or adding features
6. Update the README.md to document the new example

### Testing

Tests are minimal - primarily integration tests running example main methods. See `dl4j-examples/src/test/java/org/deeplearning4j/examples/QuickTest.java` for reference.

## Important Notes

- Each example project is **independent** - work within specific subdirectories
- CUDA support: Uncomment CUDA backend in `pom.xml` properties to use GPUs
- Memory configuration: Some examples (like VideoFrameClassifier) require significant off-heap memory (7G+)
- Historical examples in `oreilly-book-dl4j-examples` are marked as outdated in the README
- Most projects use Java 8
- Support is primarily through [community forums](https://community.konduit.ai/), not GitHub issues

## Resources

- [DL4J Documentation](https://deeplearning4j.konduit.ai/)
- [DL4J JavaDoc](http://deeplearning4j.org/doc/)
- [Maven Configuration Guide](https://deeplearning4j.konduit.ai/config/maven)
- [Memory Configuration](https://deeplearning4j.konduit.ai/config/config-memory)
- [Transfer Learning API](https://deeplearning4j.konduit.ai/tuning-and-training/transfer-learning)