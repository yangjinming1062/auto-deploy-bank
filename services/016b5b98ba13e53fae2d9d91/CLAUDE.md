# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

novel-plus v5.2.3 is a multi-end (PC/WAP) novel/ebook reading CMS system with a complete feature set for novel platforms. The system consists of:
- Frontend portal (novel-front)
- Author backend (novel-front)
- Platform admin backend (novel-admin)
- Web scraping system (novel-crawl)
- Common utilities module (novel-common)

Supports custom templates, multiple storage modes (database sharding, TXT file storage), theme switching, multi-source automatic data collection, AI writing features, membership/subscription models, and real-time statistics.

## Technology Stack

- **Java**: 21
- **Spring Boot**: 3.4.0 (parent), 2.7.18 (admin module)
- **Build Tool**: Maven
- **Database**: MySQL 8.0.29 with Sharding-JDBC 5.5.1 for sharding
- **ORM**: MyBatis 3.0.4 with Dynamic SQL 1.5.0, PageHelper 1.4.6
- **Cache**: Redis 1.4.1.RELEASE
- **Security**: Spring Security, Apache Shiro, JJWT
- **Frontend**: Thymeleaf, Layui
- **AI**: Spring AI framework with SiliconFlow API
- **Storage**: Aliyun OSS

## Architecture

### Module Structure

```
novel/
├── novel-common          # Shared utilities and common code
│   ├── core/            # Core framework (config, utils, advice, cache, enums, converter)
│   ├── entity/          # Shared entity/domain models
│   └── mapper/          # Shared MyBatis mappers
├── novel-front          # Frontend portal + Author backend
│   └── novel/           # Main package (controllers, services, mappers)
├── novel-crawl          # Web scraping service
│   └── novel/           # Scraping logic and rules
└── novel-admin          # Platform admin backend
    ├── common/          # Admin-specific common code
    ├── system/          # System management modules
    └── novel/           # Novel management modules
```

### Key Configuration Files

- `config/shardingsphere-jdbc.yml` - Database sharding configuration
- `novel-*/src/main/resources/application*.yml` - Module-specific Spring configs (dev, prod, website, alipay, oss)
- `pom.xml` - Maven build configuration with profile `central-repo` for Maven Central

### AI Features

The system integrates Spring AI for writing assistance:
- **Text Editor Integration**: AI expand, summarize, continue writing, and polish text
- **Cover Generation**: Automatic novel cover image generation based on book information
- **Default Provider**: SiliconFlow API (compatible with OpenAI)
  - Text Model: `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`
  - Image Model: `Kwai-Kolors/Kolors`

Configure AI in `novel-front/src/main/resources/application.yml`:
```yaml
spring:
  ai:
    openai:
      api-key: your-api-key
      base-url: https://api.siliconflow.cn
      chat:
        options:
          model: deepseek-ai/DeepSeek-R1-0528-Qwen3-8B
      image:
        options:
          model: Kwai-Kolors/Kolors
```

## Common Development Commands

### Build Project

```bash
# Build all modules (skips tests by default)
mvn clean install -DskipTests=true

# Build with tests
mvn clean install

# Build using central repository profile
mvn clean install -Pcentral-repo -DskipTests=true

# Build specific module
cd novel-admin && mvn clean package -DskipTests=true
```

### Database Setup

Execute SQL files in sequence:
1. Initial install: `doc/sql/novel_plus.sql`
2. Updates: Execute incremental SQL files by date (e.g., yyyyMMdd.sql)

### Running Applications

Each module has startup scripts in `src/main/build/scripts/`:

```bash
# Novel Admin (runs on port 80 by default)
./novel-admin/src/main/build/scripts/novel-admin.sh start|stop|restart|status

# Novel Front
./novel-front/src/main/build/scripts/novel-front.sh start|stop|restart|status

# Novel Crawl
./novel-crawl/src/main/build/scripts/novel-crawl.sh start|stop|restart|status
```

Or run with Spring profiles:

```bash
# Development mode
java -jar target/novel-admin.jar --spring.profiles.active=dev

# Production mode
java -jar target/novel-admin.jar --spring.profiles.active=prod

# With custom port
java -jar target/novel-admin.jar --server.port=8080
```

### Docker Deployment

Each module includes Docker support:

```bash
# Build Docker image for novel-admin
docker build -f novel-admin/src/main/build/docker/Dockerfile -t novel-admin:latest .

# Run with docker-compose (if available)
docker-compose up -d
```

### Code Generation

The project uses MyBatis Generator for DAO layer generation:
- Configure generator config in module's `src/main/resources/generator/`
- Run: `mvn mybatis-generator:generate`

## Development Notes

- **No Unit Tests**: The project has no test directory; Maven skips tests by default (`maven.test.skip=true`)
- **Version Mismatch**: Admin module uses Spring Boot 2.7.18 while parent is 3.4.0
- **Sharding Configuration**: Uses file-based sharding config at `config/shardingsphere-jdbc.yml`
- **Profile-based Configs**: Different environments use Spring profiles (dev, prod, website, alipay, oss)
- **Base Package**: All Java code is under `com.java2nb`
- **Mapper Location**: MyBatis mappers expect XML files at `mybatis/**/*Mapper.xml`

## Release Process

The project uses GitHub Actions for automated releases (see `.github/workflows/release.yml`):
1. Push tags starting with 'v' (e.g., v5.2.3)
2. GitHub Action builds with `mvn clean install -DskipTests=true -Pcentral-repo`
3. Creates release artifacts: sql.zip, novel-crawl.zip, novel-front.zip, novel-admin.zip

## Important Resources

- **Documentation**: https://docs.xxyopen.com/course/novelplus/1.html
- **Demo Site**: http://117.72.165.13:8888
- **Project Homepage**: https://novel.xxyopen.com
- **GitHub**: https://github.com/201206030/novel-plus
- **Gitee**: https://gitee.com/novel_dev_team/novel-plus

## Customization

### Adding New Modules

1. Create module directory under root
2. Add module to parent `pom.xml`
3. Configure dependencies in module's `pom.xml`
4. Create Spring Boot application class
5. Add configuration files in `src/main/resources/`

### Template System

Frontend templates are located in `/templates/` directory with theme variants:
- `dark/`
- `green/`
- `orange/`

Each theme contains static assets (CSS, JS, images) and can be customized for branding.

### Sharding Configuration

Database sharding is configured via `config/shardingsphere-jdbc.yml`. Modify this file to:
- Add/remove database nodes
- Configure sharding rules
- Adjust connection pools
- Set read/write splitting

### Scraping Rules

The novel-crawl module manages web scraping. Rules and configurations are in:
- `novel-crawl/src/main/java/com/java2nb/novel/` - Crawling logic
- Modify existing crawlers or add new source adapters as needed

## Troubleshooting

**Port Conflicts**: Admin runs on port 80 by default; change in `application.yml` or use `--server.port`

**Database Connection**: Ensure MySQL is running and accessible; verify credentials in `shardingsphere-jdbc.yml`

**Build Failures**: If Maven can't resolve dependencies, ensure you're using the `central-repo` profile or have proper mirror configuration

**AI Features Not Working**: Verify SiliconFlow API key is correctly configured in `application.yml`