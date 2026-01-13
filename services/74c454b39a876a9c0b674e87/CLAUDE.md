# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**six-realms** (六道轮回世界) is a front-end/back-end separated management system (地府管理系统). The project features:

- **Frontend**: Vue 2.5.17 + Vuex + Vue Router + Ant Design Vue
- **Backend**: Spring Boot 2.1.0 + MyBatis-Plus + MySQL + Redis + Shiro + JWT
- **Database**: MySQL 5.7.x
- **Architecture**: Traditional layered architecture with dynamic routing based on user permissions

The system implements a role-based access control with custom Vue directives for permission-based DOM rendering (`v-hasPermission`, `v-hasAnyPermission`, `v-hasRole`, `v-hasAnyRole`).

## Common Commands

### Backend (Spring Boot)

```bash
# Navigate to backend directory
cd backend

# Install dependencies (Maven will handle automatically)
mvn clean install

# Run the application
mvn spring-boot:run

# Or package and run
mvn clean package
java -jar target/thesixsectorteam-1.0.0-release.jar

# Run tests (if configured)
mvn test
```

### Frontend (Vue)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (requires Node.js >= 6.0.0, npm >= 3.0.0)
yarn install

# Start development server
yarn start
# or
npm run dev

# Build for production
yarn build
# or
npm run build

# Lint code
npm run lint
```

### Database Setup

```bash
# Import the database schema
mysql -u root -p < sql/sixsector.sql
```

## System Architecture

### Backend Structure

The backend follows a standard Spring Boot layered architecture:

```
backend/src/main/java/city/thesixsectorteam/wheelworld/
├── SixRealmsWheelWorldApplication.java    # Main application entry
├── common/                                # Shared utilities and configurations
│   ├── annotation/                        # Custom annotations
│   ├── aspect/                            # AOP aspects (LogAspect, LimitAspect)
│   ├── authentication/                    # JWT utilities
│   ├── config/                            # Spring configurations
│   ├── controller/                        # Base controllers
│   ├── domain/                            # Common DTOs and domain objects
│   ├── handler/                           # Exception handlers
│   ├── properties/                        # Configuration properties
│   ├── service/                           # Base services
│   ├── task/                              # Scheduled tasks
│   └── utils/                             # Utility classes
├── system/                                # System management module
│   ├── controller/                        # User, role, menu, dept, dict controllers
│   ├── dao/                               # MyBatis mappers
│   ├── domain/                            # System domain entities
│   ├── service/                           # System services
│   └── manager/                           # Business logic managers
├── job/                                   # Quartz job scheduling
│   ├── config/                            # Job configuration
│   ├── controller/                        # Job management
│   ├── domain/                            # Job entities
│   ├── service/                           # Job services
│   ├── task/                              # Job task implementations
│   └── util/                              # Job utilities
├── web/                                   # External API integrations
│   └── controller/                        # Weather, movie, article controllers
└── [theme-modules]/                       # Functional modules
    ├── area/                              # Area management
    ├── hadesCurrency/                     # Currency system
    ├── reincarnation/                     # Reincarnation management
    ├── soul/                              # Soul management
    ├── lifeAndDie/                        # Life/death records
    ├── trial/                             # Trial system
    ├── eighteen/                          # Eighteenth layer
    └── plague/                            # Plague records
```

**Key Backend Components:**
- **Shiro Security**: Handles authentication and authorization
- **JWT Tokens**: Stateless authentication with configurable timeout (3600s default)
- **MyBatis-Plus**: ORM with code generation support
- **Dynamic Data Source**: Supports multiple database configurations
- **AOP Logging**: Automatic operation logging (configurable via `openAopLog`)
- **Quartz Scheduler**: Task scheduling and job management
- **Redis**: Caching and session management
- **Swagger**: API documentation at `/swagger-ui.html`

### Frontend Structure

```
frontend/src/
├── components/                            # Reusable UI components
│   ├── checkbox/
│   ├── datetime/
│   ├── exception/
│   ├── menu/
│   ├── setting/
│   └── tool/
├── router/                                # Vue Router configuration
├── store/                                 # Vuex state management
│   └── modules/                           # Store modules
├── utils/                                 # Utility functions
├── views/                                 # Page components
│   ├── common/                            # Common pages
│   ├── error/                             # Error pages
│   ├── login/                             # Authentication
│   ├── monitor/                           # System monitoring
│   ├── personal/                          # User profile
│   ├── quartz/                            # Job scheduling UI
│   ├── system/                            # System management (user, role, menu, dept, dict)
│   └── web/                               # External API UI
└── App.vue                                # Root component
```

**Key Frontend Features:**
- **Dynamic Routing**: Routes built based on user permissions
- **Permission Directives**: Custom Vue directives for conditional rendering
- **Axios**: HTTP client for API communication
- **Ant Design Vue**: UI component library
- **Vuex**: State management
- **Webpack**: Build tool with dev and prod configurations

## Configuration

### Backend Configuration (`backend/src/main/resources/application.yml`)

- **Server Port**: 5432
- **Database**: MySQL (configured in `spring.datasource.dynamic.datasource.primary`)
- **Redis**: localhost:6379
- **Token Timeout**: 3600 seconds
- **Anonymous URLs**: `/login,/logout,/regist,/user/check,/swagger-resources,/webjars,/v2,/swagger-ui.html,/favicon.ico,/area/*`
- **AOP Logging**: Enabled by default (`openAopLog: true`)
- **Batch Insert Size**: 1000 records

### Frontend ESLint Configuration

The frontend uses ESLint with Vue and Standard configurations:
- Vue essential rules enabled
- Standard JavaScript style guide
- Debugger allowed in development mode only

## Default Credentials

### Demo Environment
- **scott** / **1234qwer** - Registered user (view, add, export permissions)
- **jack** / **1234qwer** - Regular user (view-only permissions)
- **sixsector** - Account deleted

### Local Environment
- **scott** / **1234qwer** - Registered user (view, add, export permissions)
- **jack** / **1234qwer** - Regular user (view-only permissions)
- **sixsector** / **liudaolunhui** - Super administrator (full permissions)

## Development Notes

1. **Lombok Required**: Install Lombok plugin in your IDE for the backend
2. **Database Setup**: Import `sql/sixsector.sql` into MySQL 5.7.x
3. **Multi-module Structure**: Backend is organized into theme-based modules (hadesCurrency, reincarnation, soul, etc.)
4. **API Documentation**: Available at `http://localhost:5432/swagger-ui.html` when backend is running
5. **P6Spy**: SQL logging is enabled by default for debugging
6. **Type Aliases**: MyBatis-Plus aliases configured for `city.thesixsectorteam.wheelworld.system.domain` and `city.thesixsectorteam.wheelworld.job.domain`

## Key System Modules

- **System Management**: User, role, menu, department, dictionary management
- **System Monitoring**: Online users, system logs, Redis monitoring, request tracing, system info (JVM, server, Tomcat)
- **Task Scheduling**: Quartz-based定时任务 (scheduled tasks) and调度日志 (dispatch logs)
- **Network Resources**: Weather queries, movie information (upcoming and now showing), daily articles
- **Functional Modules**: Area, currency, reincarnation, soul, life/death records, trial system, eighteenth layer, plague records

## Request Flow

The system implements a typical REST API flow:
1. Frontend sends request with JWT token
2. Shiro validates token and permissions
3. Request routed to appropriate controller
4. Service layer handles business logic
5. MyBatis-Plus interacts with database
6. Response returned to frontend
7. AOP logging captures operation (if enabled)