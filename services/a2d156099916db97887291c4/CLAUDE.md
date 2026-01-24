# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **WeChat Movie Ticketing System** (微麦) with three main components:
- **weapp-weimai**: WeChat mini-program for user-facing movie booking
- **film_admin**: Vue.js admin panel for platform and cinema management
- **weimai**: Spring Boot backend API

## Commands

### Backend (weimai)
```bash
# Build and run (requires MySQL, Redis, Elasticsearch running)
mvn spring-boot:run

# Build JAR
mvn package -DskipTests
```

### Admin Panel (film_admin)
```bash
cd film_admin

# Install dependencies
npm install

# Development server (hot reload)
npm run dev

# Build for production
npm run build
```

### Database Setup
```bash
# Import SQL schema (requires MySQL)
mysql -u root -p < sql/weipiao.sql
```

## Architecture

### Backend (Spring Boot)
- **Base Package**: `com.moke.wp.wx_weimai`
- **Controllers**: `/home` (public), `/admin` (authenticated/shiro)
- **Services**: Separate service classes for each domain (MovieService, CinemaService, OrderService, etc.)
- **Mappers**: MyBatis-Plus mappers in `mapper/` directory
- **Entities**: Domain models and VOs in `entity/` directory
- **Key Config**: `config/` contains Shiro auth, Redis, Elasticsearch, Mahout recommendation configs

### Admin Frontend (Vue.js)
- **Pages**: `src/pages/Home/` (platform admin), `src/pages/Business/` (cinema operator)
- **API**: `src/api/index.js` - centralized API exports
- **AJAX**: `src/api/ajax.js` - Axios wrapper with base URL `https://mokespace.cn/weimai`
- **Router**: `src/router/index.js` - defines `/login`, `/home/*`, `/business/*` routes

### WeChat Mini-program
- **Pages**: `pages/home/`, `pages/cinema/`, `pages/user/`, `pages/subPages/` (movie details, seat selection, orders, etc.)
- **Global Data**: `app.js` - stores userInfo, userLocation, selectCity, and API base URL
- **Utils**: `utils/util.js` - formatting utilities and throttling helper

## API Conventions

### Backend Endpoints
- **Public APIs**: `/home/*` (movie list, banners, search, cinema info)
- **Admin APIs**: `/admin/*` (require authentication via Shiro)
- **Response Format**: `Result` class with `code`, `data`, `msg` fields

### Frontend API Calls
- Admin panel uses custom `ajax()` wrapper in `src/api/ajax.js`
- Mini-program uses `wx.request` directly to `https://mokespace.cn/weimai`

## Dependencies

### Infrastructure Required
- MySQL 5.7+ (database: `weipiao`)
- Redis (port 6379, password: 123456, database: 1)
- Elasticsearch (cluster: docker-cluster, port 9300)

### External Services
- Tencent Maps SDK for location reverse geocoding (configured in `weapp-weimai/app.js`)
- WeChat API (mini-program appId: wxb367811c1b81b819)

## Key Features

- **Movie Recommendations**: Uses Apache Mahout for user-based collaborative filtering
- **Location-based Search**: Elasticsearch with geo-queries for nearby cinema discovery
- **Role-based Access**: Two admin roles - platform admin (`/home/*`) and cinema operator (`/business/*`)