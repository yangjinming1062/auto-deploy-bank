# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

轻阅读 (QRead) is a backend service for a novel reading application that syncs across mobile, web, and desktop clients. It provides REST APIs for book search, reading progress synchronization, and book source management.

## Build Commands

```bash
# Build the project (outputs to libs/ directory with dependencies)
./gradlew build

# Build only the book library module
cd book && ../gradlew build

# Clean build artifacts
./gradlew clean
```

## Running the Application

```bash
# Build first, then run
./gradlew build
java -jar libs/solon-read-1.0-SNAPSHOT.jar

# Or with custom port
java -Dserver.port=8080 -jar libs/solon-read-1.0-SNAPSHOT.jar

# With proxy (for testing from restricted networks)
java -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=1080 -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=1080 -jar libs/solon-read-1.0-SNAPSHOT.jar
```

## Architecture

### Project Structure

- **`book/`** - Core library module for web scraping and rule-based content extraction
  - `book/model/` - Data models (Book, BookSource, BookChapter, etc.)
  - `book/webBook/` - Web scraping engines (WBook, BookInfo, BookChapterList, BookContent)
  - `book/util/` - Utilities (HTTP, encoding, file, HTML processing)
  - `book/util/help/` - Helper classes for cookies, caching, source analysis
  - `book/icu4j/` - Charset detection for content encoding

- **`src/main/kotlin/web/`** - Solon web application
  - `web/App.kt` - Application entry point with Solon startup
  - `web/controller/` - REST API controllers
    - `api/` - Public API endpoints (versioned at `/api/{v}`)
    - `admin/` - Admin dashboard endpoints
  - `web/model/` - Database entities (MyBatis-Plus models)
  - `web/mapper/` - MyBatis-Plus mappers for database access
  - `web/cron/` - Scheduled jobs (book updates, cache cleanup, RSS refresh)
  - `web/notification/` - WebSocket notification handlers
  - `web/response/` - API response wrappers

### Key Data Flows

1. **Book Search**: `BookController.searchBook` → `WBook.searchBook` → executes source-specific JS rules with JsoupXpath
2. **Content Reading**: `ReadController.getBookContent` → `BookContent.getbookcontent` → applies replace rules → returns cached/processed content
3. **Source Management**: Sources stored in DB with JSON config; parsed by `BookSource.fromJson()` at runtime

### Source Rules System

Book sources use JSON configuration with JavaScript functions for:
- `searchBook` - Search for books by keyword
- `exploreBook` - Browse books by category/explore rules
- `getBookInfo` - Extract book metadata from detail page
- `getChapterList` - Extract chapter list from TOC page
- `getChapterContent` - Extract chapter content with paywall handling

Sources execute in a Rhino JS environment with access to Java methods like `java.get()`, `java.post()`, `java.cookie()`, and unique proxy functions (`java.getusePhone()`).

### Database

- SQLite (default) or MySQL (configurable via `conf.yml` / environment variables)
- MyBatis-Plus with AutoTable for schema management
- Key tables: `users`, `booklist`, `book_source`, `user_book_source`, `replace_rule`, `book_cache`

### Configuration

Configuration via `conf.yml` or environment variables:
- `DB_TYPE` - sqlite/mysql
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` - Admin credentials
- `SERVER_HTTP_CORETHREADS` / `SERVER_HTTP_MAXTHREADS` - Thread pool settings
- `USER_SOURCE` - 0=read-only, 1=admin editable, 2=user private sources

## API Versioning

All API endpoints are versioned at `/api/{v}` where `v` must match `apiversion` (currently 5). Controllers check version compatibility.

## WebSocket Endpoints

- `/api/{v}/ws` - General API WebSocket
- `/api/{v}/debug` - Source debugging
- `/api/{v}/rssdebug` - RSS source debugging
- `/api/{v}/checkdebug` - Source validation debugging

## Response Format

All APIs return JSON with format:
```json
{
  "isSuccess": true/false,
  "errorMsg": "error message if failed",
  "data": { ... }
}
```

## Common Patterns

- Controllers extend `BaseController` for authentication helpers (`getuserbytocken`, `getsource`, `getBookSourcelist`)
- `@CrossOrigin(origins = "*")` enables open CORS
- Cache service using `@Cache` and `@CacheRemove` annotations
- Scheduled tasks via `@EnableScheduling` with `@Scheduled` methods
- Replace rules applied via regex with timeout protection (`RegexTimeoutException`)