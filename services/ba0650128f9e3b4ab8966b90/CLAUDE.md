# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Architecture

This project is a multi-module Maven project that implements a SonarQube plugin for analyzing Java code. The main plugin is in the `sonar-java-plugin` module. Other modules provide checks, a test kit, and integration tests.

## Common Commands

### Build

To build the project and run unit tests, use the following command from the root directory:

```bash
mvn clean install
```

**Note:** You need Java 23 to build the project.

### Running Integration Tests

To run the integration tests, you need Java 17.

#### Sanity Test

This test runs all checks against all test source files without taking into account the result of the analysis. It verifies that rules are not crashing on any file in our test sources.

```bash
mvn clean install -P sanity
```

#### Plugin Test

This is an integration test suite that verifies plugin features such as metric calculation, coverage, etc.

```bash
mvn clean install -Pit-plugin -DcommunityEditionTestsOnly=true
```

#### Ruling Test

This integration test suite launches the analysis of a large code base, saves the issues created by the plugin in report files, and then compares those results to the set of expected issues.

First, make sure the submodules are checked out:

```bash
git submodule update --init --recursive
```

Then, from the `its/ruling` folder, launch the ruling tests:

```bash
mvn clean install -Pit-ruling -DcommunityEditionTestsOnly=true
```

#### Autoscan Test

These tests are designed to detect differences between the issues the Java analyzer can find with and without bytecode.

First, compile the test sources in the `java-checks-test-sources` module:

```bash
# Use java 24!
mvn clean compile
```

Then, to run the tests, move to the `its/autoscan` folder and run:

```bash
# cd its/autoscan
# use Java 17!
mvn clean package --batch-mode --errors --show-version \
   --activate-profiles it-autoscan \
  -Dsonar.runtimeVersion=LATEST_RELEASE
```
