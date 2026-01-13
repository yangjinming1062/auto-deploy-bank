# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

HiBench is a Big Data benchmark suite (version 8.0-SNAPSHOT) that evaluates different big data frameworks including Hadoop, Spark, Flink, Storm, and Gearpump. It contains 29 workloads across 6 categories: micro, ml (machine learning), sql, graph, websearch, and streaming.

## Common Commands

### Build
```bash
# Build entire project
bin/build_all.sh

# Or use Maven directly
mvn clean package

# Build specific module
cd sparkbench && mvn clean package
cd hadoopbench && mvn clean package
cd flinkbench && mvn clean package
cd stormbench && mvn clean package
cd gearpumpbench && mvn clean package
```

### Run Benchmarks
```bash
# Run all enabled benchmarks (reads conf/benchmarks.lst and conf/frameworks.lst)
bin/run_all.sh

# Run single workload
bin/workloads/micro/wordcount/prepare/prepare.sh
bin/workloads/micro/wordcount/spark/run.sh

# Generate reports
bin/report_gen_plot.py
```

### CI/CD Testing
The project uses GitHub Actions with 6 workflow files testing different version combinations:
- Spark 2.4 + Hadoop 2.7
- Spark 3.0 + Hadoop 3.2
- Spark 3.1 + Hadoop 3.2

## High-Level Architecture

### Maven Modules
- **`common/`** - Shared utilities and components used across all benchmarks
- **`autogen/`** - Data generation tools for benchmarks
- **`sparkbench/`** - Apache Spark workloads (largest module)
  - Subdirectories: `micro/`, `ml/`, `sql/`, `graph/`, `streaming/`, `structuredStreaming/`
  - Assembly JAR: `sparkbench/assembly/target/sparkbench-assembly-*-dist.jar`
- **`hadoopbench/`** - Apache Hadoop MapReduce workloads
  - Subdirectories: `mahout/`, `nutchindexing/`, `pegasus/`, `sql/`
- **`flinkbench/`** - Apache Flink streaming workloads
- **`stormbench/`** - Apache Storm streaming workloads
- **`gearpumpbench/`** - Apache Gearpump streaming workloads

### Configuration System
- **`conf/hibench.conf`** - Main runtime configuration (131 lines)
  - Scale profiles: tiny, small, large, huge, gigantic, bigdata
  - HDFS paths and directory structures
  - JAR path definitions
  - Current default scale: `tiny` (line 3)
- **Framework templates** in `conf/`:
  - `spark.conf.template`, `hadoop.conf.template`
  - `flink.conf.template`, `storm.conf.template`, `gearpump.conf.template`
- **`conf/benchmarks.lst`** - Lists 29 enabled benchmarks
- **`conf/frameworks.lst`** - Lists enabled frameworks (hadoop, spark)

### Execution Framework
- **`bin/`** - Shell scripts for orchestration
  - `build_all.sh` - Triggers Maven build for all modules
  - `run_all.sh` - Orchestrates benchmark execution
  - `functions/` - Shared shell functions
  - `workloads/` - Per-workload execution scripts organized by category
  - `report_gen_plot.py` - Report generation and visualization

### Supported Versions
- **Hadoop:** 2.x, 3.0.x, 3.1.x, 3.2.x, CDH5, HDP
- **Spark:** 2.4.x, 3.0.x, 3.1.x
- **Flink:** 1.0.3
- **Storm:** 1.0.1
- **Gearpump:** 0.8.1
- **Kafka:** 0.8.2.2 (for streaming benchmarks)

### Workload Categories (29 total)

**Micro Benchmarks (6):** Sort, WordCount, TeraSort, Repartition, Sleep, Enhanced DFSIO

**Machine Learning (13):** Bayes, K-means, Gaussian Mixture, Logistic Regression, ALS, Gradient Boosted Trees, XGBoost, Linear Regression, LDA, PCA, Random Forest, SVM, SVD

**SQL (3):** Scan, Join, Aggregation

**Websearch (2):** PageRank, Nutch Indexing

**Graph (1):** NWeight

**Streaming (4):** Identity, Repartition, Stateful Wordcount, Fixed Window

## Documentation References

- **Build Guide:** `docs/build-hibench.md`
- **Hadoop Benchmarks:** `docs/run-hadoopbench.md`
- **Spark Benchmarks:** `docs/run-sparkbench.md`
- **Streaming Benchmarks:** `docs/run-streamingbench.md`
- **Docker Guide:** `docker/README.md`
- **Framework Configuration:** `docs/*-configuration.md`

## Docker Support

Three Docker variants available:
- **`docker/base/`** - Base image
- **`docker/cdh-docker/`** - Cloudera Distribution
- **`docker/opensource-docker/`** - Apache Hadoop/Spark
- Configuration: `docker/hibench-docker.conf`