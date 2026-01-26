# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Neuroph is a Java neural network platform consisting of two main components:
- **neuroph-2.9/**: Maven-based core framework (neural network library)
- **NeurophStudio/**: NetBeans Platform-based GUI application

This is a legacy repository. New development has moved to:
- https://github.com/neuroph/NeurophFramework (core framework)
- https://github.com/neuroph/NeurophStudio (GUI)

## Build Commands

### Neuroph Core Framework (neuroph-2.9)

```bash
# Build all modules
cd neuroph-2.9 && mvn clean install

# Compile without installing
mvn compile

# Run all tests
mvn test

# Run a single test class
mvn test -Dtest=NeuralNetworkTest

# Run a specific test method
mvn test -Dtest=NeuralNetworkTest#testCreate

# Generate JavaDoc
mvn javadoc:javadoc

# Generate code coverage report (Cobertura)
mvn cobertura:cobertura
```

### NeurophStudio (NetBeans Platform)

NeurophStudio uses the NetBeans Platform build system. Open the `NeurophStudio` folder in NetBeans IDE, which will recognize it as a module suite project.

## Architecture

### Core Framework (neuroph-2.9/Core)

The neural network framework follows a layered architecture:

```
org.neuroph.core
├── NeuralNetwork<L>     - Base class for all neural networks, contains Layers and LearningRule
├── Layer                - Container for neurons
├── Neuron               - Individual neuron with input/output functions
├── Connection           - Weighted connection between neurons
├── input                - Input functions (WeightedSum, Sum, Product, etc.)
├── transfer             - Transfer functions (Sigmoid, Tanh, Linear, etc.)
└── learning             - Learning rules (BackPropagation, PerceptronLearning, etc.)

org.neuroph.nnet
├── MultiLayerPerceptron - Standard MLP network
├── ConvolutionalNetwork - CNN for image processing
├── RBFNetwork          - Radial Basis Function network
├── Hopfield            - Hopfield associative memory
├── Kohonen             - Self-organizing map
├── ElmanNetwork        - Recurrent network
└── JordanNetwork       - Recurrent network

org.neuroph.util
├── DataSet              - Training data container
├── plugins              - Plugin infrastructure (PluginBase)
└── random               - Weight randomizers

org.neuroph.eval
└── Evaluation           - Network evaluation utilities
```

### Key Design Patterns

- **NeuralNetwork**: Generic base class parameterized with LearningRule type
- **Layer**: Contains neurons; supports different neuron types via NeuronFactory
- **LearningRule**: Iterative learning with epoch-based training
- **TransferFunction**: Pluggable activation functions
- **InputFunction**: Pluggable input aggregation functions
- **PluginBase**: Extensible plugin system for adding behavior to networks

### GUI Architecture (NeurophStudio)

Built on NetBeans Platform with modular structure:
- Each folder under `NeurophStudio/` is a NetBeans module
- `SDK Core/`, `SDK Engine/`, `SDK Libraries/` contain platform dependencies
- Modules are loaded by NetBeans module system at runtime

## Key Files

- `neuroph-2.9/pom.xml` - Parent Maven POM for all framework modules
- `neuroph-2.9/Core/pom.xml` - Core framework module configuration
- `neuroph-2.9/Core/src/test/java/` - JUnit test cases
- `NeurophStudio/nbproject/project.xml` - NetBeans module suite configuration

## Testing Stack

- JUnit 4.10 for unit testing
- Mockito 1.9.5 for mocking
- PowerMock 1.5.4 for static method mocking
- Cobertura for code coverage

## Dependencies

Framework dependencies (managed via Maven):
- SLF4J 1.7.5 + Logback for logging
- Apache Commons Lang 3.3.2

## Data Format

- Neural networks are serialized using Java serialization
- DataSets use custom file formats via `org.neuroph.util.io` adapters
- Supports file, URL, JDBC, and stream-based data I/O