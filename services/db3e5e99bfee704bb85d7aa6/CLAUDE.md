# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

**Installation:**
- Install the package: `pip install -U crawl4ai`
- For pre-release versions: `pip install crawl4ai --pre`
- Run post-installation setup: `crawl4ai-setup`
- Verify your installation: `crawl4ai-doctor`

**Development Installation:**
- Clone the repository: `git clone https://github.com/unclecode/crawl4ai.git`
- Install in editable mode: `cd crawl4ai && pip install -e .`

**Running the CLI:**
- Basic crawl: `crwl https://www.example.com -o markdown`
- Deep crawl: `crwl https://docs.crawl4ai.com --deep-crawl bfs --max-pages 10`
- LLM extraction: `crwl https://www.example.com/products -q "Extract all product prices"`

**Docker:**
- Pull and run the Docker image: `docker pull unclecode/crawl4ai:0.7.0 && docker run -d -p 11235:11235 --name crawl4ai --shm-size=1g unclecode/crawl4ai:0.7.0`
- Visit the playground: `http://localhost:11235/playground`

## High-Level Code Architecture and Structure

Crawl4AI is a Python-based web crawler and scraper designed to be friendly for Large Language Models (LLMs). It can be used as a library or through its command-line interface.

**Core Concepts:**
- **`AsyncWebCrawler`:** The main class for performing asynchronous crawling.
- **`CrawlerRunConfig`:** Configuration for a specific crawl run, including caching, markdown generation, and extraction strategies.
- **Extraction Strategies:** Pluggable strategies for extracting structured data from web pages. `JsonCssExtractionStrategy` for CSS selectors and `LLMExtractionStrategy` for using LLMs.
- **Adaptive Crawling:** The crawler can learn and adapt to website patterns to explore only what matters.
- **Docker Deployment:** The project includes a Dockerfile and a pre-built Docker image for easy deployment.
