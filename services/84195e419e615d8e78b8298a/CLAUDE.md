# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FlyCms is a Chinese Q&A-based social networking CMS built with Spring Boot. It's a community platform similar to Zhihu, featuring questions & answers, articles, user management, and admin backend. The project is primarily developed in Chinese.

**Technology Stack:**
- JDK 8, Spring Boot 2.0.3
- MyBatis ORM with MySQL database
- Solr for full-text search
- Freemarker templating engine
- Ehcache for caching
- Jetty embedded server
- Bootstrap 3 frontend
- Quartz for scheduled tasks
- Shiro for permissions

## Common Commands

### Building the Project
```bash
# Clean and compile
mvn clean compile

# Package the application
mvn clean package

# Build with assembly plugin (recommended for production)
mvn clean package assembly:single

# This creates target/FlyCms.jar with dependencies in target/dist/
```

### Running the Application

**Prerequisites:**
1. MySQL database `flycms` must exist (UTF-8 or UTF8MB4 charset)
2. Solr server must be running on port 8983 (see Setup below)
3. Import the database schema from `doc/flycms_date.sql`

**Development mode:**
```bash
# Run with default profile
mvn spring-boot:run

# Or run the JAR directly
java -jar target/FlyCms.jar
```

**Production mode:**
```bash
# Create production config
cp src/main/resources/application.yml src/main/resources/application-prod.yml
# Edit application-prod.yml with production settings

# Run with production profile
java -jar FlyCms.jar --spring.profiles.active=prod
```

### Solr Setup (Required for Search)

**Windows:**
```bash
# Navigate to Solr installation
cd e:/solr/bin
solr start -p 8983
# To stop: solr stop -p 8983
```

**Linux:**
```bash
cd /root/webapp/solr
./bin/solr start -p 8983 -force
# To stop: ./bin/solr stop -p 8983 -force
```

If search fails, clear Solr data: `E:\solr\server\solr\info\data` (delete the three folders)

### Database Operations
```bash
# Import schema and initial data
mysql -u root -p flycms < doc/flycms_date.sql

# Default admin login:
# URL: http://localhost/system/login
# Username: flycms
# Password: 123456

# Frontend access:
# URL: http://localhost
```

### Service Management
```bash
# Stop the service
ps -ef | grep FlyCms.jar | grep -v grep | cut -c 9-15 | xargs kill -s 9

# View logs
tail -200f FlyCms.log
```

### Testing
```bash
# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=ClassName

# Run with Maven
mvn -Dtest=UserServiceTest test
```

## Architecture Overview

### Directory Structure
```
src/main/java/com/flycms/
├── Application.java              # Main Spring Boot application
├── core/                         # Core utilities and base classes
│   ├── base/
│   │   └── BaseController.java   # Base controller with common methods
│   ├── controller/               # Global controllers
│   ├── entity/                   # Data transfer objects (DataVo, PageVo)
│   ├── exception/                # Custom exceptions
│   ├── service/                  # Global services
│   └── utils/                    # Utility classes
├── module/                       # Feature modules
│   ├── admin/                    # Admin management
│   ├── article/                  # Article/blog system
│   ├── config/                   # Configuration management
│   ├── favorite/                 # User favorites
│   ├── job/                      # Scheduled tasks (Quartz)
│   ├── links/                    # Friend links
│   ├── message/                  # Messaging system
│   ├── order/                    # Orders
│   ├── other/                    # Miscellaneous
│   ├── question/                 # Q&A system
│   ├── score/                    # Points/scoring
│   ├── search/                   # Search integration
│   ├── share/                    # Content sharing
│   ├── template/                 # Theme templates
│   ├── topic/                    # Topics
│   ├── user/                     # User management
│   ├── websocket/                # WebSocket support
│   └── weight/                   # Weight/ranking
├── web/                          # Web controllers
│   ├── front/                    # Frontend public controllers
│   ├── system/                   # Admin backend controllers
│   └── tags/                     # Custom Freemarker tags
├── config/                       # Configuration classes
├── constant/                     # Constants
├── filter/                       # Servlet filters
└── interceptor/                  # Interceptors

views/
├── static/                       # Static assets (CSS, JS, images)
└── templates/                    # Freemarker templates
    ├── pc_theme/                 # Frontend templates
    │   └── defalut/
    └── system/                   # Admin templates
        ├── admin/
        ├── common/
        └── ...

src/main/resources/
├── application.yml               # Main configuration
├── ehcache.xml                   # Cache configuration
├── i18n/                         # Internationalization
│   ├── messages_zh_CN.properties
│   └── messages_en_US.properties
└── log4j2.xml                    # Logging configuration
```

### Module Organization

Each module follows a consistent pattern:
- `dao/` - MyBatis mapper interfaces and XML files
- `model/` - Entity models (POJOs)
- `service/` - Business logic services
- Optional: Controller files in respective `web/` subdirectories

### Layer Architecture

**Three-tier architecture:**
1. **Controller Layer** (`web/`)
   - Frontend controllers in `web/front/` (public endpoints)
   - Admin controllers in `web/system/` (authenticated endpoints)
   - All controllers extend `BaseController`

2. **Service Layer** (`module/*/service/`)
   - Business logic and transaction management
   - Caching annotations (`@Cacheable`, `@CacheEvict`)
   - Integration with DAO layer

3. **DAO Layer** (`module/*/dao/`)
   - MyBatis mapper interfaces
   - XML mapper files in `src/main/resources/com/flycms/module/**/dao/*.xml`
   - Database operations

### Key Components

**BaseController** (`src/main/java/com/flycms/core/base/BaseController.java`)
- Provides common functionality to all controllers
- `getUser()` - retrieves current frontend user
- `getAdminUser()` - retrieves current admin user
- Injects common services (UserService, AdminService, TemplateService)

**Template System** (`module/template/service/TemplateService`)
- Manages theme switching between PC and mobile
- `theme.getPcTemplate(view)` - renders PC theme templates
- `theme.getAdminTemplate(view)` - renders admin templates
- Templates are in `views/templates/pc_theme/defalut/` and `views/templates/system/`

**Database Configuration**
- Uses Druid connection pool (configured in `application.yml`)
- MyBatis with XML mappers
- Auto-scan: `com.flycms.module.**.dao`
- Entity aliases: `com.flycms.module.**.model`

**Caching** (Ehcache)
- Configured in `ehcache.xml`
- Named caches: `config`, `user`, `article`, `question`, `share`, `areas`
- Spring `@Cacheable` annotations on service methods

**Search Integration**
- Solr server at `http://127.0.0.1:8983/solr/info`
- Used for full-text search and content listing
- IK Analyzer for Chinese text processing

## Development Notes

### IDE Requirements
- **Lombok plugin required** - IDE will show errors without it
- Configure annotation processing for Lombok
- Supports IntelliJ IDEA and Eclipse

### Configuration Profiles
- `application.yml` - Default/dev settings
- `application-prod.yml` - Production settings (create manually)
- Use `--spring.profiles.active=prod` to activate

### Database Notes
- Currently optimized for **MySQL 5.7**
- To support emojis, use `utf8mb4` charset
- Default admin: username `flycms`, password `123456`
- Schema file: `doc/flycms_date.sql`

### Third-party Dependencies
- **Aliyun SMS** (Alibaba Dayu) - Requires manual JAR installation
  - Download `dysmsapi.zip` from `doc/`
  - Install to local Maven: `.m2/repository/com/alibaba/aliyun/`

### Internationalization
- Chinese and English support
- Files in `src/main/resources/i18n/`
- Session-based language switching via `/checklanguage/{cn|us}`

### Permission System
- Shiro-based permission framework
- Admin roles and permissions in `fly_admin_group_*` tables
- Permission sync available via `/system/admin/permission_sync`

## Access URLs

**Frontend:**
- Homepage: `http://localhost`
- Explore: `http://localhost/explore/`

**Admin Backend:**
- Login: `http://localhost/system/login`
- Dashboard: `http://localhost/system/`

**Error Pages:**
- 403: `http://localhost/403`
- 404: `http://localhost/404`
- 500: `http://localhost/500`

## Custom Tags Example

```freemarker
<@fly_userpower groupName="技术专家组">
    <nav class="list-group mt30">
        <a href="/ucenter/article/add" class="list-group-item active">发布文章</a>
    </nav>
</@fly_userpower>
```

## Key Features

**Frontend Features:**
- Q&A system with rewards/points
- Article/blog publishing with expert columns
- Content sharing (files, resources)
- Topic aggregation
- User profiles and collections
- Points/credit system
- Mobile registration, email registration
- Password recovery

**Admin Features:**
- User management and approval
- Content moderation (questions, answers, articles)
- Topic management
- Points/credit rule configuration
- Scheduled task management (Quartz)
- Keyword filtering
- SMS/email configuration
- Site configuration

## Important Notes

1. **Solr is required** - Application will error without running Solr server
2. **Lombok required** - Install plugin in IDE before importing
3. **Database charset** - Use `utf8mb4` to support emojis
4. **Session management** - Frontend users and admin users use separate sessions
5. **Theme customization** - Templates in `views/templates/pc_theme/defalut/`
6. **Chinese project** - Most comments, logging, and UI text are in Chinese
7. **Version** - Built on Spring Boot 2.0.3 (older version, consider upgrading)

## Database Schema

Key tables:
- `fly_admin` - Admin users
- `fly_user` - Frontend users
- `fly_question` - Questions
- `fly_answer` - Answers
- `fly_article` - Articles
- `fly_article_category` - Article categories
- `fly_topic` - Topics
- `fly_share` - Shared content
- `fly_config` - System configuration

Full schema in: `doc/flycms_date.sql`