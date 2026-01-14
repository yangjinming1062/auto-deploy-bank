# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese word segmentation (CWS) evaluation framework that compares the accuracy and performance of multiple Chinese text segmenters. It provides tools to evaluate segmentation quality against gold-standard annotated text and measure processing speed.

## Build Commands

```bash
# Build the project
mvn clean install

# Run full evaluation (assesses all segmenters)
mvn exec:java -Dexec.mainClass="org.apdplat.evaluation.Evaluator"

# Run interactive segmenter comparison (enter Chinese text for side-by-side comparison)
mvn exec:java -Dexec.mainClass="org.apdplat.evaluation.WordSegmenter"

# Or use shell scripts (Linux)
./evaluation.sh
./contrast.sh
```

**Note**: Stanford segmenter requires extensive memory. Set `MAVEN_OPTS="-Xms3000m -Xmx3000m"` before running.

## Architecture

### Core Interfaces and Classes

- **`Segmenter`** (`org.apdplat.evaluation.Segmenter`): Interface contract for text segmentation
- **`Evaluation`** (`org.apdplat.evaluation.Evaluation`): Abstract base class containing common evaluation logic (file I/O, report generation, speed measurement)
- **`Evaluator`** (`org.apdplat.evaluation.Evaluator`): Main entry point that discovers and runs all Evaluation implementations
- **`WordSegmenter`** (`org.apdplat.evaluation.WordSegmenter`): Interface for segmenters that support multiple algorithm comparison

### Segmenter Implementations

Located in `org.apdplat.evaluation.impl` package. Each segmenter extends `Evaluation` and implements the segmentation interface:

- `WordEvaluation` - word分词器 with multiple algorithms
- `AnsjEvaluation` - ansj分词器 (BaseAnalysis, ToAnalysis, NlpAnalysis, IndexAnalysis)
- `HanLPEvaluation` - HanLP分词器
- `MMSeg4jEvaluation` - mmseg4j分词器 (SimpleSeg, ComplexSeg, MaxWordSeg)
- `SmartCNEvaluation` - Lucene smartcn
- `JiebaEvaluation` - jieba分词器 (SEARCH, INDEX)
- `JcsegEvaluation` - jcseg分词器 (简易模式, 复杂模式)
- `IKAnalyzerEvaluation` - IKAnalyzer (智能切分, 细粒度切分)
- `FudanNLPEvaluation` - FudanNLP
- `StanfordEvaluation` - Stanford segmenter (Chinese Treebank, Beijing University)

### Data Files

- `data/test-text.txt`: Unsegmented test corpus (2.5M lines, 28M characters)
- `data/standard-text.txt`: Gold-standard segmented text (word boundaries with spaces)
- `data/speed-test-text.txt`: Large text for pure speed benchmarking
- `report/`: Output directory for evaluation reports (`分词效果评估报告.txt`)

### Evaluation Process

1. `Evaluator.main()` discovers all `Evaluation` implementations via classpath reflection
2. Each evaluation calls `segFile()` to segment the test corpus and measure speed
3. Results are compared against standard text to calculate perfect/line and perfect/char rates
4. `Evaluation.generateReport()` produces sorted comparison reports

## Running Specific Evaluations

Exclude specific segmenters by passing class names as arguments:

```bash
mvn exec:java -Dexec.mainClass="org.apdplat.evaluation.Evaluator" -Dexec.args="WordEvaluation HanLPEvaluation"
```