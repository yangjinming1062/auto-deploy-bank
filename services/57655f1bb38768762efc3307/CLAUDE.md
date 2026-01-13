# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

crawler4j is an open-source Java web crawling library that provides a simple interface for crawling the Web with multi-threaded support. The project is structured as a Gradle multi-module build with the main library (`crawler4j`) and example projects.

## Architecture

The crawler4j library follows a modular architecture with these key components:

### Core Components (crawler4j module)

1. **crawler** - Main crawling logic
   - `CrawlController.java:49` - Orchestrates crawling sessions, manages crawler threads, monitors progress
   - `WebCrawler.java:50` - Base class for user-defined crawlers; handles URL processing and page visits
   - `CrawlConfig.java` - Configuration settings for crawling behavior

2. **fetcher** - HTTP page fetching
   - `PageFetcher.java` - Handles HTTP requests using Apache HttpClient
   - `PageFetchResult.java` - Encapsulates fetch results

3. **frontier** - URL queue management
   - `Frontier.java` - Manages the crawl queue using Berkeley DB
   - `DocIDServer.java` - Assigns unique IDs to URLs
   - `Counters.java` - Tracks crawling statistics

4. **parser** - Content parsing
   - `Parser.java` - Entry point for parsing content using Apache Tika
   - `HtmlParseData.java` - HTML-specific parse data with text, links, and metadata
   - `TextParseData.java`, `BinaryParseData.java`, `CssParseData.java` - Other content types

5. **robotstxt** - Robots.txt compliance
   - `RobotstxtServer.java` - Checks if URLs are allowed by robots.txt
   - `RobotstxtParser.java` - Parses robots.txt files

6. **url** - URL handling
   - `WebURL.java` - Represents a URL with metadata (depth, docid, etc.)
   - `URLCanonicalizer.java` - URL normalization and canonicalization

7. **util** - Utility classes
   - `IO.java`, `Util.java`, `Net.java` - Helper functions

### Persistence Layer

The crawler uses **Berkeley DB (JE)** for persistent storage:
- Crawl frontier (URL queue)
- DocID-to-URL mappings
- Crawl statistics and counters
- Enables resumable crawling across restarts

### Data Flow

```
Seeds → Frontier Queue → Crawler Threads → PageFetcher → Content → Parser → shouldVisit() → visit()
                                ↓
                          robots.txt Server
```

## Common Commands

### Build and Compilation
```bash
./gradlew clean build          # Clean and build all modules
./gradlew :crawler4j:build     # Build only the main library
```

### Testing
```bash
./gradlew test                 # Run all tests
./gradlew :crawler4j:test      # Run tests for main library only
./gradlew test --tests "*PageFetcherHtmlTest"    # Run specific test class
```

### Code Quality
```bash
./gradlew checkstyle           # Run Checkstyle on all modules
./gradlew :crawler4j:checkstyleMain  # Check main code only
./gradlew :crawler4j:checkstyleTest  # Check test code only
```

### Running Examples

The examples are located in `crawler4j-examples/` directory:

```bash
# Build examples
./gradlew :crawler4j-examples-base:build

# Run specific examples (from the respective module)
cd crawler4j-examples/crawler4j-examples-base
./gradlew run --args="basic.BasicCrawler"
```

### Publishing
```bash
./gradlew publishToMavenLocal   # Publish to local Maven repository
```

## Example Usage Pattern

Users create crawlers by extending `WebCrawler` and implementing:
- `boolean shouldVisit(Page referringPage, WebURL url)` - Filter URLs to crawl
- `void visit(Page page)` - Process downloaded pages

The controller is configured with `CrawlConfig` and manages the crawling lifecycle via `CrawlController.start()`.

## Key Dependencies

- Apache HttpClient 4.5.7 - HTTP fetching
- Apache Tika 1.20 - Content parsing (HTML, PDF, binary)
- Berkeley DB JE 18.3.12 - Persistent storage
- SLF4J + Logback - Logging
- Google Guava 27.0.1 - Utilities

## Configuration

Important configuration options in `CrawlConfig`:
- `setMaxDepthOfCrawling(int)` - Limit crawl depth
- `setMaxPagesToFetch(int)` - Limit total pages
- `setPolitenessDelay(int)` - Delay between requests (ms)
- `setIncludeHttpsPages(boolean)` - Enable HTTPS crawling
- `setIncludeBinaryContentInCrawling(boolean)` - Crawl binary files
- `setResumableCrawling(boolean)` - Enable resumable crawling
- `setProxyHost/Port()` - Configure proxy
- `setUserAgentString(String)` - Custom user agent