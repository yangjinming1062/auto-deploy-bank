# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CRMEB Java is a full-featured open-source e-commerce system built with:
- **Backend**: Java SpringBoot 2.2.6, MyBatis Plus, MySQL 5.7+, Redis
- **Admin Frontend**: Vue 2.x + Element UI (PC management console)
- **Mobile Frontend**: Uni-app (H5 + WeChat Mini Program)

The system supports multiple business models including new retail, distribution, group buying, flash sales, and more.

## Repository Structure

```
crmeb/                     # Java SpringBoot backend
├── crmeb-front/          # Main application (REST API)
├── crmeb-admin/          # Admin interface API
├── crmeb-service/        # Shared business logic
├── crmeb-common/         # Common utilities and models
├── shell/                # Deployment scripts
└── sql/                  # Database schema (Crmeb_1.3.4.sql)

admin/                    # Vue 2.x admin panel
├── src/
│   ├── api/             # API endpoints
│   ├── components/      # Reusable components
│   ├── views/           # Page components
│   ├── router/          # Vue Router config
│   ├── store/           # Vuex store
│   ├── utils/           # Utilities
│   └── permission.js    # Authentication logic

app/                      # Uni-app mobile application
├── pages/               # Mobile pages
├── components/          # Custom components
├── api/                 # API calls
├── js_sdk/              # JavaScript SDK
└── store/               # Pinia/Vuex store

接口文档/                  # API documentation
```

## Technology Stack

### Backend (crmeb/)
- **Framework**: SpringBoot 2.2.6.RELEASE
- **Build Tool**: Maven 3.6.1
- **Database ORM**: MyBatis Plus 3.3.1
- **API Docs**: Swagger 2.9.2 + Swagger Bootstrap UI 1.9.3
- **Data Source**: Druid 1.1.20 (Alibaba)
- **Cache**: Redis (with Jedis client)
- **Validation**: javax.validation 1.1.0.Final
- **Utils**: Hutool 4.5.7, Apache Commons Lang3

### Admin Frontend (admin/)
- **Framework**: Vue 2.6.10
- **UI Library**: Element UI 2.13.0
- **State Management**: Vuex 3.1.0
- **HTTP Client**: Axios 0.24.0
- **Build Tool**: Vue CLI 3.5.3
- **Charts**: ECharts 4.2.1
- **Testing**: Jest (Vue Test Utils)

### Mobile Frontend (app/)
- **Framework**: Uni-app
- **Build System**: HBuilderX
- **Platforms**: H5, WeChat Mini Program, App

## Common Commands

### Backend (Java/SpringBoot)

```bash
# Navigate to backend directory
cd crmeb/

# Build the project
mvn clean package -Dmaven.test.skip=true

# Run with profiles (dev/staging/prod)
java -jar crmeb-front/target/crmeb-front.jar --spring.profiles.active=prod

# Or use the provided shell scripts
cd crmeb/shell/
./startFront.sh    # Start the API server
./stopFront.sh     # Stop the API server
./startAdmin.sh    # Start admin API (if separate)
./stopAdmin.sh     # Stop admin API

# Default API URL: http://localhost:8081
# Swagger API Docs: http://localhost:8081/doc.html
```

### Admin Frontend (Vue)

```bash
# Navigate to admin directory
cd admin/

# Install dependencies
npm install

# Development server
npm run dev        # Starts on port 9527

# Build for production
npm run build:prod

# Build for staging
npm run build:stage

# Run tests
npm run test:unit

# Lint code
npm run lint

# CI test (lint + unit tests)
npm run test:ci

# Generate new component (using Plop)
npm run new
```

### Mobile Frontend (Uni-app)

```bash
# Navigate to app directory
cd app/

# Install dependencies (if needed)
npm install

# Build for different platforms using HBuilderX:
# - H5:发行->发行H5
# - WeChat:发行->发行微信小程序
# - App:发行->原生App-云打包/本地打包

# Or use CLI (if configured)
# npm run build:h5
# npm run build:mp-weixin
```

## Configuration

### Backend Configuration

**Database & Redis** (`crmeb-front/src/main/resources/application.yml`):
- MySQL: `jdbc:mysql://127.0.0.1:3306/crmeb`
- Default credentials: username=`crmeb`, password=`111111`
- Redis: `127.0.0.1:6379`, password=`111111`, database=3
- Default port: `8081`

**Application Settings**:
- Server port: `8081` (configurable in application.yml)
- File upload: Max 50MB per file
- Context path: `/` (root)
- Time zone: `GMT+8`

### Admin Frontend Configuration

**Build Configuration** (`admin/vue.config.js`):
- Dev server port: `9527` (configurable via `port` env var)
- Public path: `/` (for deployment)
- Output directory: `dist`
- Source maps disabled in production

**Runtime Configuration** (`admin/src/settings.js`):
- Site title: `CRMEB` (customizable)

### Mobile Frontend Configuration

**App Configuration** (`app/manifest.json`):
- App ID, name, and version
- Uni-app runtime configuration
- Platform-specific settings

## Development Workflow

### Backend Development

The backend follows standard SpringBoot architecture:

1. **Controllers** (`crmeb-front/src/main/java/com/zbkj/front/controller/`): Handle HTTP requests
2. **Services** (`crmeb-front/src/main/java/com/zbkj/front/service/`): Business logic
3. **ServiceImpl** (`crmeb-front/src/main/java/com/zbkj/front/service/impl/`): Service implementations
4. **Models**: Located in `crmeb-common` module
5. **Mappers**: MyBatis Plus interfaces for database access

Key modules:
- `crmeb-common`: Shared DTOs, entities, constants, utils
- `crmeb-service`: Shared business logic across modules
- `crmeb-admin`: Admin-specific API endpoints
- `crmeb-front`: Public-facing API endpoints (storefront)

### Frontend Development

**Admin Panel (Vue)**:
- Uses Vue Router for navigation
- Vuex for state management
- Element UI components
- Features include:
  - Authentication & authorization (Spring Security integration)
  - Dashboard with ECharts statistics
  - Product management
  - Order management
  - User management
  - System configuration
  - Form generator (drag-and-drop form builder)

**Mobile App (Uni-app)**:
- Page-based architecture
- Custom components
- API integration layer
- Responsive design for multiple platforms

## Key Features

1. **Multi-tenant E-commerce Platform**:
   - Products, categories, inventory management
   - Shopping cart, orders, payments
   - User accounts, points, coupons
   - Marketing: flash sales, group buying, promotions

2. **Admin Management**:
   - Role-based access control (Spring Security)
   - Statistics dashboard with ECharts
   - System configuration management
   - Drag-and-drop form generator

3. **Mobile Support**:
   - H5 web app
   - WeChat Mini Program
   - Native app builds (via Uni-app)

4. **Integrations**:
   - Multiple cloud storage providers (Aliyun OSS, Tencent COS, Qiniu)
   - Printer support (Yilianyun)
   - Product data source (Tmall, JD, Taobao, etc.)

## Database

- **Schema**: Initial setup in `crmeb/sql/Crmeb_1.3.4.sql`
- **ORM**: MyBatis Plus with code generation support
- **Features**:
  - Logical deletion (isDel field)
  - Global configuration in application.yml
  - SQL logging enabled in debug mode

## API Documentation

- Swagger UI: http://localhost:8081/doc.html
- Swagger configuration in application.yml
- API endpoints grouped by functionality
- JWT-based authentication

## Testing

### Backend
```bash
# Run unit tests
mvn test

# Run specific test
mvn test -Dtest=ClassName#methodName
```

### Admin Frontend
```bash
# Unit tests with Jest
npm run test:unit

# Watch mode
npm run test:unit -- --watch
```

## Deployment

### Backend Deployment

1. Build the JAR:
   ```bash
   cd crmeb/
   mvn clean package -Dmaven.test.skip=true
   ```

2. Upload `crmeb-front/target/crmeb-front.jar` to server

3. Configure environment-specific properties (application-prod.yml)

4. Run with shell script:
   ```bash
   ./startFront.sh
   ```

5. Check logs:
   ```bash
   tail -f crmeb_out.log
   ```

### Frontend Deployment

1. **Admin**:
   ```bash
   cd admin/
   npm run build:prod
   # Deploy dist/ to web server (Nginx/Apache)
   ```

2. **Mobile**:
   - Build using HBuilderX
   - Deploy H5 to web server
   - Upload mini program to WeChat platform
   - Build native app for app stores

## Important Notes

- **Default credentials**: Admin demo `admin/123456`, Mobile demo `18292417675/Crmeb_123456`
- **Port 20000**: Cannot be used for the backend service
- **Environment**: Java 1.8+, MySQL 5.7+, Redis 5+
- **API Documentation**: Enable in application.yml (currently set to `debug: true`)
- **CORS**: Configure in SpringBoot for cross-origin requests
- **File Storage**: Configure cloud storage credentials in system config table

## Common Development Tasks

### Adding a New Backend API

1. Create Controller in appropriate module (admin/front)
2. Create Service interface and implementation
3. Create/Update MyBatis Mapper if needed
4. Update database schema (if necessary)
5. Document API with Swagger annotations
6. Update frontend API client

### Adding a New Admin Page

1. Create route in `admin/src/router/index.js`
2. Create view component in `admin/src/views/`
3. Create API client in `admin/src/api/`
4. Add to menu in permission/role config
5. Test with Vue dev server

### Adding a New Mobile Page

1. Create page in `app/pages/`
2. Add to `app/pages.json`
3. Create API integration
4. Update navigation/routes
5. Test in HBuilderX

## Troubleshooting

**Backend won't start**:
- Check MySQL and Redis are running
- Verify database credentials in application.yml
- Check port conflicts (8081 or 20000)
- Review logs in `crmeb_out.log`

**Admin frontend build fails**:
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version (requires >= 8.9, npm >= 3.0.0)
- Clear Jest cache: `jest --clearCache`

**API calls failing**:
- Verify backend is running on correct port
- Check CORS configuration
- Verify API base URL in frontend config
- Check authentication token validity