# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build and run tests
mvn clean package

# Build without running tests
mvn clean package -DskipTests

# Install to local Maven repository
mvn install

# Run basepom checks (checkstyle, findbugs, etc.)
mvn verify
```

## Project Architecture

SlimFast is a multi-module Maven project with two modules that replace fat jars with a classpath-based approach:

### slimfast-plugin
Maven plugin with three goals that manage dependency artifacts:

- **copy goal** (`CopyJarsMojo`): Copies runtime dependency jars to a local directory. Runs during the `package` phase. Uses `ArtifactHelper` to extract classpath entries from the maven-jar-plugin manifest configuration.

- **upload goal** (`UploadJarsMojo`): Uploads dependencies to S3 during the `deploy` phase. Only uploads files that don't already exist in S3 (skip-if-exists logic). Outputs a JSON manifest (`target/slimfast.json`) listing all uploaded artifacts.

- **download goal** (`DownloadJarsMojo`): Standalone goal that downloads dependencies from S3 using the manifest file. Can run without a `pom.xml` using Maven's `exec:java` style invocation.

Key plugin classes:
- `BaseUploadMojo`: Abstract base for upload operations; handles S3 configuration, file uploader instantiation, and dry-run mode
- `ArtifactHelper`: `@Singleton` that parses maven-jar-plugin manifest configuration and computes artifact paths using Maven's repository layout patterns
- `S3Factory`: Creates AWS S3 clients with configurable credentials and region
- `FileUploader`/`FileDownloader`: Pluggable interfaces; `DefaultFileUploader` uses AWS S3 Transfer Manager, `DryRunFileUploader` logs without uploading

### slimfast-hadoop
Lightweight library for Hadoop jobs to avoid fat jars. Contains:

- `HadoopHelper`: Static utility that finds dependency jars via `Class-Path` manifest entries, copies them to HDFS (only if absent), and adds them to `mapreduce.job.classpath.files` and `mapreduce.job.cache.files` configuration properties.

- `SlimfastHadoopConfiguration`: Builder-based configuration for `HadoopHelper`, requiring the main job jar and Hadoop `Configuration`.

## Key Dependencies

- **basepom (65.2)**: Parent POM providing checkstyle, findbugs, and other standard checks
- **AWS SDK (v2)**: S3 client via `s3` and `s3-transfer-manager` modules
- **Plexus (plexus-utils, plexus-interpolation)**: Dependency injection and path interpolation for artifact layout computation
- **Guava**: Utility library used throughout