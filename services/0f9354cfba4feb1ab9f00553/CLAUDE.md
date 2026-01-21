# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Teaching Open** v2.8 is a STEAM online education platform for institutions and schools, providing a cost-effective solution for educational administration. The platform integrates CRM, educational administration, assignments, question bank, competitions, community, and article systems.

- **Live Demo:** http://open.teaching.vip
- **Official Website:** http://teaching.vip
- **QQ Group:** 191723983

## Technology Stack

### Backend (Java/Spring Boot)
- **Framework:** Spring Boot 2.1.3.RELEASE
- **Language:** Java 8
- **Persistence:** MyBatis-Plus 3.1.2
- **Security:** Apache Shiro 1.4.0 + JWT 3.7.0
- **Database:** MySQL 5.6+ (supports Oracle, SQL Server, PostgreSQL)
- **Cache:** Redis 6.0
- **Build:** Maven

### Frontend (Vue.js)
- **Framework:** Vue 2.6.10
- **UI Library:** Ant Design Vue 1.6.3
- **Build Tool:** Vue CLI 3.3.0, Webpack
- **Linting:** ESLint 5.16.0

## Common Development Commands

### Backend (in api/ directory)

```bash
# Install dependencies and build
mvn clean package

# Run application (after build)
java -jar jeecg-boot-module-system/target/jeecg-boot-module-system-2.8.0.jar

# Development (in IDE)
# Run org.jeecg.JeecgApplication main method
```

**Note:** Tests are currently disabled in the Maven build (see api/pom.xml).

### Frontend (in web/ directory)

```bash
# Install dependencies
npm install
# or
yarn install

# Development server (http://localhost:8000)
npm run serve
# or
yarn run serve

# Production build
npm run build
# or
yarn run build

# Lint code
npm run lint
# or
yarn run lint

# Run single test (if tests are added)
npm run test -- --testNamePattern="test-name"
```

### Dev Server Proxy
The frontend dev server proxies API calls:
- `/api/*` → `http://localhost:8081`

## High-Level Architecture

### Backend Architecture (Multi-module Maven)

```
api/
├── db/                              # Database migrations
│   ├── teachingopen2.8.sql          # Base schema v2.8
│   └── update2.2.sql → update2.8.sql # Version upgrades
├── jeecg-boot-base-common/          # Shared utilities, annotations
└── jeecg-boot-module-system/        # Main application
    ├── config/                      # Spring configurations
    │   ├── MybatisPlusConfig.java
    │   ├── ShiroConfig.java         # Security configuration
    │   ├── Swagger2Config.java      # API documentation
    │   └── RedisConfig.java
    ├── modules/                     # Business modules
    │   ├── system/                  # System management
    │   ├── teaching/                # Teaching features
    │   └── ngalain/                 # NgAlain integration
    └── JeecgApplication.java        # Spring Boot entry point
```

### Frontend Architecture (Vue SPA)

```
web/
├── public/                          # Static assets
│   ├── scratch3/                    # Scratch 3.0 integration
│   ├── scratchjr/                   # ScratchJr integration
│   ├── python/                      # Python Turtle
│   ├── blockly/                     # Blockly editor
│   └── tinymce/                     # Rich text editor
└── src/
    ├── views/                       # Page components
    │   ├── account/                 # Account management
    │   ├── dashboard/               # Dashboard
    │   ├── system/                  # System admin
    │   ├── teaching/                # Teaching modules
    │   └── jeecg/                   # JEECG components
    ├── components/                  # Reusable components
    │   ├── jeecg/                   # JEECG form/table
    │   └── chart/                   # Charts
    ├── router/                      # Vue Router config
    ├── api/                         # API services
    ├── store/                       # Vuex state management
    └── utils/                       # Utilities
```

### Educational Tools Integration

The platform includes integrated programming tools:
- **Scratch 3.0** - Visual programming blocks
- **ScratchJr** - Visual programming for younger students
- **Python Turtle** - Python programming environment
- **Blockly** - Google's visual programming editor

## Development Environment Setup

### Backend Requirements
1. **Java 8** - `yum install -y java-1.8.0-openjdk` (CentOS)
2. **MySQL 5.6+** - Required: `lower_case_table_names=1` in my.cnf
3. **Redis 6.0**
4. **Maven** - Use Aliyun mirror in `settings.xml`

### Frontend Requirements
1. **Node.js v12** (for npm compatibility)
2. **npm** or **yarn**

### Additional Services
- **Qiniu Cloud Storage** - For file uploads and media assets
  - Required: accessKey, secretKey, bucketName, staticDomain
  - Alternative: local storage (not recommended for production)

## Configuration

### Backend Configuration Files

- `application-dev.yml` - Development environment
- `application-prod.yml` - Production environment (default)
- `application.yml` - Base configuration

Key configuration sections in `application-prod.yml`:
```yml
# Domain and upload settings
domain: your-domain.com
uploadType: qiniu  # or local

# Database
datasource:
  master:
    url: jdbc:mysql://127.0.0.1:3306/teachingopen
    username: teachingopen
    password: teachingopen

# Redis
redis:
  database: 1
  host: 127.0.0.1
  port: 6379

# Qiniu
qiniu:
  accessKey: your-accessKey
  secretKey: your-secretKey
  bucketName: your-bucket
  staticDomain: your-domain.com
```

### Frontend Configuration Files

- `vue.config.js` - Webpack configuration with theme customization
- `babel.config.js` - Babel configuration
- `package.json` - Dependencies and scripts

## Database Migrations

Migration files are in `api/db/`:
- **Base:** `teachingopen2.8.sql`
- **Upgrades:** `update2.2.sql` → `update2.8.sql` (sequential for upgrades)

**Note:** Table names are case-insensitive (required by MySQL configuration).

## Key Features

### User Roles
- **admin** - Super administrator
- **teacher** - Teacher
- **student** - Student
Default password for all test accounts: `123456`

### Core Modules
- Homepage and dashboard
- Community system
- Creative tools (Scratch, Python, ScratchJr, Blockly)
- Student center (works, assignments, courses)
- Assignment and course management
- Article/news management
- System administration (users, roles, permissions, classes)

## Testing

### Test Accounts
- Admin: `admin` / `123456`
- Teacher: `teacher` / `123456`
- Student: `student` / `123456`

### Manual Testing
- Backend API: http://localhost:8080 (when running)
- Frontend: http://localhost:8000 (dev server)
- Production: http://open.teaching.vip (demo)

## Deployment

### Backend Deployment
1. Build: `mvn clean package` in api/
2. Upload jar + yml config to server
3. Run: `nohup java -jar teaching-open-xxx.jar &`

### Frontend Deployment
1. Build: `npm run build` in web/
2. Upload `dist/` to web server root
3. Configure Nginx (see README.md for config)

### Nginx Configuration
The production setup requires:
- SPA routing support (rewrite to index.html)
- Gzip compression
- API proxy to backend: `location ^~ /api`

## Troubleshooting

### Page Loading Continuously
1. Check if API is running: http://ip:8080
2. Verify Nginx proxy configuration (502/504 errors)

### Scratch Assets Not Displaying
- Custom assets require Qiniu cloud storage
- Upload `scratch3/static/internalapi` to Qiniu
- Update `scratch3/index.html` assetHost configuration

### Scratch Submission Stuck
- Check Qiniu configuration (other uploads will also fail)
- Session timeout - save locally and resubmit
- Network issues

### System Upgrades
1. Execute upgrade SQL files sequentially
2. Stop old API: `pkill java`
3. Upload new jar and restart
4. Rebuild and upload frontend `dist/`

## Version History

- **v2.8** - Article/news system, work tagging, customizable homepage
- **v2.7** - Mobile UI optimization, Blockly editor, role-level permissions
- **v2.6** - Custom assignments, online configuration, map editor
- Earlier versions focused on Scratch integration and core features

## Important Notes

1. **Storage:** Qiniu cloud storage is strongly recommended for production
2. **MySQL:** Case-insensitive table names required
3. **Node Version:** Use Node.js v12 for frontend compatibility
4. **Tests:** Currently disabled in backend build
5. **Security:** JWT-based authentication with Shiro
6. **Documentation:** Extensive Chinese documentation in README.md files

## Key Files

- `/README.md` - Comprehensive deployment and architecture guide (Chinese)
- `/api/README.md` - Backend development guide
- `/web/README.md` - Frontend development guide
- `/changelist.txt` - Version history
- `/web/vue.config.js` - Frontend build configuration
- `/api/pom.xml` - Backend Maven configuration
- `/api/db/` - Database migration files