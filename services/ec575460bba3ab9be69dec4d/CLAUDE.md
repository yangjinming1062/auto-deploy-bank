# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dagli is a machine learning framework for Java 9+ that represents ML pipelines as directed acyclic graphs (DAGs). A DAG defines the pipeline once for both training and inference—no separate training vs inference pipeline is needed.

## Build Commands

```bash
# Build and test the entire project
./gradlew build

# Build without running tests
./gradlew assemble

# Run tests (JUnit 5)
./gradlew test

# Run tests including expensive/extensive tests
./gradlew build -Palltests

# Run a specific test class
./gradlew :module-name:test --tests "ClassName"

# Checkstyle validation
./gradlew checkstyleMain checkstyleTest

# Generate IntelliJ project files
./gradlew idea

# Publish to Maven Central (requires credentials)
./gradlew uploadArchives --no-daemon --no-parallel
```

## Key Architecture Concepts

### DAG Structure
- **Root nodes**: `Placeholder`s (data inputs) and `Generator`s (auto-generated values like `Constant`, `IndexGenerator`)
- **Child nodes**: `Transformer`s that transform inputs from parent nodes
- **PreparableTransformer**: Examines training data to create a `PreparedTransformer`
- **PreparedTransformer**: Ready-to-use transformer for inference
- **View**: Extracts information from a prepared transformer during training

### Core Base Classes
- `AbstractPreparedTransformerN` (arity 1-10) for prepared transformers
- `AbstractBatchPreparerN` / `AbstractStreamPreparerN` for preparable transformers
- `AbstractPreparedStatefulTransformerN` for transformers needing minibatching/caching

### Key Interfaces
- `Producer<T>`: Base interface for all nodes that produce values
- `PreparableTransformer`: Can be prepared to yield a `PreparedTransformer`
- `PreparedTransformer`: Immediately usable transformer

### Transformer Design Requirements
Transformers must be:
1. **Immutable**: Properties cannot change after creation (return copies)
2. **Thread-safe**: Usable by multiple threads without locking
3. **Serializable**: Entire DAGs serialize as single objects
4. **Quasi-deterministic**: Same inputs yield equally valid outputs

## Module Organization

- **core**: Base DAG classes, transformers, placeholders, generators
- **common**: Most transformers (feature transformations, evaluation, meta-transformers)
- **math-vector**: `Vector` implementations for feature vectors and embeddings
- **objectio-***: Data serialization (Avro, Kryo, BigList readers/writers)
- **text-tokenization**: `Tokens` transformer for text tokenization
- **nn / nn-dl4j**: Neural network abstraction and DL4J implementation
- **xgboost**: XGBoost classification/regression models
- **liblinear**: Logistic regression classifier
- **fasttext**: FastText text classification
- **calibration**: Isotonic regression for probability calibration
- **visualization-***: DAG visualization (ASCII, Mermaid)

## Common Development Patterns

### Creating a Prepared Transformer
Extend `AbstractPreparedTransformerN` with `@ValueEquality` annotation. Use `clone()` for immutable setters:

```java
@ValueEquality
public class MyTransformer extends AbstractPreparedTransformer1<Input, Output> {
    private static final long serialVersionUID = 1;
    private boolean _option = false;

    public MyTransformer withOption(boolean option) {
        return clone(c -> c._option = option);
    }

    public Output apply(Input input) { ... }
}
```

### Testing Transformers
Use `com.linkedin.dagli.tester.Tester` for convenient testing:

```java
Tester.of(new MyTransformer())
    .input(value1)
    .input(value2)
    .expectedOutput(result1)
    .expectedOutput(result2)
    .test();
```

### Input Configuration
Use input configurators for convenient input setup:
```java
new LiblinearClassification<LabelType>()
    .withLabelInput(label)
    .withFeaturesInput().fromNumbers(float1, float2, float3)
    .withFeaturesInput().combining().fromVectors(vector).done();
```

## Gradle Configuration Notes

- Java 9+ required (JDK 1.9 configured)
- Uses Gradle daemon for faster local builds
- Parallel builds enabled by default
- Large heap size (4g) for tests
- Some tests skipped unless `-Palltests` is passed