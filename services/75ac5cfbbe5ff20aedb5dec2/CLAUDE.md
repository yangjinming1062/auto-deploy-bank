# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-module Maven project demonstrating how to deploy machine learning models to Apache Kafka Streams for real-time inference. Each module showcases a different ML framework integrated with Kafka Streams.

## Build Commands

```bash
# Build all modules
mvn clean package

# Build a specific module (run from module directory)
mvn clean package

# Run unit tests for a specific module
mvn test

# Run a single test class
mvn test -Dtest=Kafka_Streams_MachineLearning_H2O_GBM_ExampleTest

# Build fat JAR (with dependencies) for deployment
mvn package -DskipTests
```

## Project Structure

```
kafka-streams-machine-learning-examples/
├── pom.xml                    # Parent POM (multi-module)
├── h2o-gbm/                   # Module 1: H2O GBM for flight delay prediction
├── tensorflow-image-recognition/  # Module 2: TensorFlow CNN for image recognition
├── dl4j-deeplearning-iris/    # Module 3: DeepLearning4J for Iris classification
└── tensorflow-keras/          # Module 4: Keras model import via DL4J
```

## Architecture

Each module follows a consistent pattern:
1. **Kafka Streams Topology**: `KStream` reads from input topic, applies ML inference via `mapValues()`, writes to output topic
2. **Pre-trained Models**: Stored in `src/main/resources/generatedModels/` - included in repo
3. **Main Application Class**: Extends or uses `StreamsBuilder` to define topology
4. **Input/Output Topics**: Each module defines INPUT_TOPIC and OUTPUT_TOPIC constants

### Module Details

| Module | ML Framework | Input | Use Case |
|--------|-------------|-------|----------|
| h2o-gbm | H2O GBM | CSV flight data | Predict flight delays |
| tensorflow-image-recognition | TensorFlow 1.3 | Image file paths | Image classification (Inception CNN) |
| dl4j-deeplearning-iris | DeepLearning4J | Iris measurements | Iris species prediction |
| tensorflow-keras | Keras→DL4J import | Unknown | Model import demonstration |

### Key Dependencies

- **Kafka**: `kafka-streams:2.5.0`
- **Confluent**: `5.5.0` (for schema registry in tests)
- **Java Version**: 1.8 (Java 8 required)

## Testing Pattern

Tests use two approaches:

1. **Unit Tests**: `TopologyTestDriver` - lightweight, no Kafka broker needed
   - Location: `src/test/java/.../*Test.java`
   - Pattern: `pipeInput()` → verify `readOutput()`

2. **Integration Tests**: `EmbeddedKafkaCluster` - full Kafka integration
   - Location: `src/test/java/.../*IntegrationTest.java`

Example test pattern from `h2o-gbm`:
```java
testDriver.pipeInput(recordFactory.create(INPUT_TOPIC, null, "1987,10,14,3,741,..."));
assertThat(getOutput()).isEqualTo("Prediction: Is Airline delayed? => YES");
```

## Manual Testing

To run a full Kafka Streams application (requires running Kafka broker):

```bash
# Build fat JAR first
mvn package -DskipTests

# Start Kafka (e.g., Confluent CLI)
confluent local start kafka

# Create topics
kafka-topics --bootstrap-server localhost:9092 --create --topic AirlineInputTopic --partitions 3
kafka-topics --bootstrap-server localhost:9092 --create --topic AirlineOutputTopic --partitions 3

# Run application
java -cp h2o-gbm/target/h2o-gbm-*.jar com.github.megachucky.kafka.streams.machinelearning.Kafka_Streams_MachineLearning_H2O_GBM_Example

# Send test data
echo "1987,10,14,3,741,730,912,849,PS,1451,NA,91,79,NA,23,11,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,YES,YES" | kafkacat -b localhost:9092 -P -t AirlineInputTopic

# Consume predictions
kafka-console-consumer --bootstrap-server localhost:9092 --topic AirlineOutputTopic --from-beginning
```

## Common Package Structure

Main source packages:
- `com.github.megachucky.kafka.streams.machinelearning` - Application classes
- `com.github.megachucky.kafka.streams.machinelearning.models` - Generated ML model POJOs

## Important Notes

- Models are pre-trained and included in `src/main/resources/generatedModels/` - no training required
- The TensorFlow image recognition example uses a private `GraphBuilder` helper class for model construction
- H2O examples use `EasyPredictModelWrapper` for simplified inference
- Tests use `EmbeddedSingleNodeKafkaCluster` utilities from Confluent for integration testing