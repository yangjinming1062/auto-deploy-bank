# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lilishop is a comprehensive B2B2C e-commerce system built with Spring Boot (Java 8) for the backend and Vue/uni-app for the frontend. The project supports multi-tenant merchant access and distributed deployment with microservices architecture.

## Architecture Overview

### Backend Modules (Maven Modules)
- **buyer-api** - Customer-facing APIs for shopping functionality
- **seller-api** - Merchant-facing APIs for store management
- **manager-api** - Platform admin APIs
- **common-api** - Shared API components and utilities
- **im-api** - Instant messaging APIs
- **framework** - Core framework, shared utilities, database configs, and infrastructure code
- **consumer** - Message queue consumers (RocketMQ)
- **admin** - Admin portal frontend (Vue.js)

### Core Dependencies & Technologies
- **Spring Boot 2.4.10** - Core framework
- **Mybatis-Plus 3.5.5** - ORM framework
- **Spring Security + JWT** - Authentication & authorization
- **MySQL** - Primary database (via ShardingSphere for horizontal scaling)
- **Redis + MongoDB** - Caching and storage
- **Elasticsearch** - Search engine
- **RocketMQ** - Message queue for async operations
- **XXL-Job 2.3.0** - Distributed task scheduling

### Configuration Structure
Key configuration files:
- **config/application.yml** - Main application configuration (database, Redis, MQ, ES, etc.)
- **pom.xml** - Maven parent POM with all dependencies
- **deploy-api.yml** - Deployment configuration

## Common Development Commands

### Building & Testing
```bash
# Build all modules (skips tests by default)
mvn clean package -DskipTests

# Build specific module
mvn clean package -pl buyer-api -am -DskipTests

# Run tests
mvn test

# Run tests for specific module
mvn test -pl buyer-api

# Build and create Docker images
./docker-image.sh
```

### Running Individual Services
```bash
# Run buyer API
cd buyer-api && mvn spring-boot:run

# Run manager API
cd manager-api && mvn spring-boot:run

# Run seller API
cd seller-api && mvn spring-boot:run
```

### Database Operations
- Database migration scripts are in **DB/** directory
- Version-specific upgrade scripts: `version{X}to{Y}.sql`
- Initial data scripts: `li_notice_message.sql`

### Service Dependencies
Required services (configured in config/application.yml):
- **MySQL 5.7+** (port 30306)
- **Redis** (port 30379)
- **Elasticsearch** (port 30920)
- **RocketMQ** (port 9876)
- **XXL-Job Admin** (port 30001)

## Code Structure Patterns

### API Module Structure
Each API module follows this structure:
```
src/
├── main/
│   ├── java/cn/lili/
│   │   ├── controller/     # REST controllers
│   │   ├── service/        # Business logic
│   │   ├── entity/         # Data models
│   │   └── mapper/         # Data access
│   └── resources/
│       └── mapper/         # MyBatis XML files
└── test/
    └── java/               # Unit tests
```

### Framework Components
**framework** module contains:
- **cn.lili.elasticsearch** - ES configuration and utilities
- **cn.lili.mybatis** - Database utilities, sharding configs
- **cn.lili.rocketmq** - MQ tags and producers
- **cn.lili.modules** - Common business components

### Key Configuration Locations
- **config/application.yml:171-178** - MyBatis configuration
- **config/application.yml:180-194** - Logging configuration
- **config/application.yml:196-198** - Jasypt encryption config
- **config/application.yml:201-289** - Application-specific settings
- **config/application.yml:56-108** - ShardingSphere database config

## Security & Authentication

### Authentication Flow
- JWT-based authentication
- Token expiration: 30 minutes (configurable in config/application.yml:245)
- Spring Security for access control
- Sensitive URLs listed in config/application.yml:110-158

### Security Configuration
- JWT settings in config/application.yml:243-245
- Security ignored URLs in config/application.yml:110-158
- Sensitive data masking level: config/application.yml:218

## API Documentation

### Swagger/OpenAPI
- Swagger UI available at `/doc.html`
- API version in config/application.yml:163
- Contact info in config/application.yml:166-168

### API Endpoints by Module
- **Buyer APIs** (customer-facing): `/buyer/*`
- **Seller APIs** (merchant-facing): `/seller/*`
- **Manager APIs** (admin-facing): `/manager/*`
- **Common APIs**: `/common/*`
- **IM APIs**: `/im/*`

## Message Queue & Async Operations

### RocketMQ Topics (config/application.yml:271-289)
- `shop_lili_promotion_topic` - Promotion activities
- `shop_lili_goods_topic` - Goods-related events
- `shop_lili_order_topic` - Order processing
- `shop_lili_member_topic` - Member operations
- `shop_lili_notice_topic` - Notification events
- `shop_lili_after_sale_topic` - After-sale processing

## Deployment

### Docker Deployment
```bash
# Build and push Docker images
./docker-image.sh

# Deploy using compose configuration
docker-compose -f deploy-api.yml up -d
```

### Production Considerations
- Configure load balancer (Nginx recommended)
- Set up database replication/clustering
- Configure message queue clusters
- Set up monitoring and logging
- Configure CDN for static assets

## Important Configuration Values

### Jasypt Encryption
- Encryption password: config/application.yml:198
- Used for encrypting sensitive configuration values

### Cache Settings
- Redis cache timeout: config/application.yml:250
- Cache enabled: config/application.yml:175

### Thread Pool
- Core size: config/application.yml:253
- Max size: config/application.yml:254
- Queue capacity: config/application.yml:255

## Development Guidelines

### Adding New APIs
1. Place in appropriate module based on user type
2. Follow RESTful conventions
3. Implement proper error handling
4. Document with Swagger annotations
5. Add to security configuration if needed

### Database Changes
1. Create migration script in DB/ directory
2. Follow naming pattern: `version{X}to{Y}.sql`
3. Test migration on clean database

### Testing
- Write unit tests in src/test/java
- Test both success and error scenarios
- Use @SpringBootTest for integration tests

## Environment Setup Requirements

- JDK 1.8+
- Maven 3.x
- MySQL 5.7+
- Redis
- RocketMQ
- Elasticsearch
- Node.js 12+ (for frontend builds)

## Troubleshooting

### Common Issues
1. **Database connection failed**: Check config/application.yml:63-65
2. **Redis connection failed**: Check config/application.yml:31-44
3. **MQ connection failed**: Check config/application.yml:290-295
4. **SQL logging**: Enable in config/application.yml:107

### Logs Location
- Application logs: `logs/` directory (config/application.yml:188)
- XXL-Job logs: config/application.yml:306

## Cursor Rules

The project includes Cursor development rules in `.cursor/rules/`:
- **01-project-overview.mdc** - Module descriptions
- **02-technical-architecture.mdc** - Tech stack details
- **03-development-guidelines.mdc** - Development practices
- **04-deployment-guide.mdc** - Deployment procedures