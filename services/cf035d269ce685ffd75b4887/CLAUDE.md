# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SOKLIB is a Knowledge Base Management System built with Java 8 using the SSM stack (Spring + Spring MVC + MyBatis). The system features full-text search with Chinese NLP support, document recommendation using collaborative filtering, and multimedia processing capabilities.

## Build Commands

```bash
# Build WAR file
mvn clean package

# Run tests (note: skipTests=true by default in pom.xml)
mvn test

# Run with embedded Jetty
mvn jetty:run

# Generate MyBatis mapper code
mvn mybatis-generator:generate
```

## Architecture

The application follows a standard layered architecture:

```
src/main/java/com/lib/
├── dao/          # MyBatis mapper interfaces
├── entity/       # Database entities (e.g., UserInfo, FileInfo, DocInfo)
├── service/      # Business logic (user/ and admin/ subpackages)
│   └── impl/     # Service implementations
├── web/          # Spring MVC controllers (admin/ and user/ subpackages)
│   └── interceptor/  # AdminInterceptor, UserInterceptor for role-based access control
└── utils/        # Utilities (Mahout recommendation, TextRank, TF-IDF)
```

### Access Control
- `AdminInterceptor`: Restricts admin URLs to users with admin privileges
- `UserInterceptor`: Manages user session and authentication state

## Key Technology Integration

### Full-Text Search
- **Lucene 5.1.0** with **HanLP** and **IKAnalyzer** for Chinese tokenization
- Configuration: `src/main/resources/hanlp.properties`
- Index service: `com.lib.service.user.LuceneService`

### Document Recommendation
- **Apache Mahout 0.7** collaborative filtering
- Table: `file_score` in MySQL, storing user-document interactions
- Service: `com.lib.service.user.AdminCountService`

### Document Processing
- **OpenOffice/JODConverter** for Office-to-PDF conversion
- **FFmpeg** for video compression and thumbnail extraction
- **Apache Tika** for text extraction from various formats
- **iTextPDF** for PDF generation
- **ICEpdf** for PDF thumbnail generation
- **Apache POI** for Office document parsing

### Key Utility Classes
| Class | Purpose |
|-------|---------|
| `LuceneIndexUtil` / `LuceneSearchUtil` | Full-text search index management |
| `MahoutRecommender` | Collaborative filtering recommendations |
| `FileManagerController` | File uploads, ZIP/RAR extraction |

## Database Configuration

Database and connection pool settings are in `src/main/resources/jdbc.properties`. The application uses:
- MySQL database named `lib`
- Druid connection pool
- MyBatis mappers in `src/main/resources/mapper/`

## Local File Storage

The application requires a local file storage path (default: `D://soklib/`) configured in `jdbc.properties`. This path stores uploaded files, converted documents, and thumbnails.

## Core Configuration Files

| File | Purpose |
|------|---------|
| `src/main/resources/jdbc.properties` | Database connection and file storage path |
| `src/main/resources/hanlp.properties` | Chinese NLP dictionary paths |
| `src/main/resources/spring/spring-dao.xml` | MyBatis and data source configuration |
| `src/main/resources/spring/spring-web.xml` | MVC, interceptors, and web configuration |
| `src/main/resources/mybatis-config.xml` | MyBatis global settings |

## System Initialization

On first run, the system initializes via `InitController` (`/init/start`):
- Creates the default admin account
- Initializes root knowledge categories