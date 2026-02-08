# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pharmacy Management System - A full-stack Angular 8 application with Node.js/Express backend and MongoDB database. Features include inventory management, point of sale, doctor orders, supplier management, sales reporting, and ML-based prediction charts using TensorFlow.js/Brain.js.

## Common Commands

```bash
# Install dependencies
npm install

# Run development servers
ng serve                    # Frontend at http://localhost:4200
npm run start:server        # Backend at http://localhost:3000

# Build and test
ng build                    # Production build to dist/pro
ng test                     # Unit tests via Karma
ng e2e                      # End-to-end tests via Protractor
ng lint                     # Lint with tslint

# Generate Angular artifacts
ng generate component component-name
ng generate service service-name
ng generate module module-name
```

## Architecture

### Frontend (Angular 8)
- **Module Structure**: Single `AppModule` declares ~80 components across feature directories
- **Routing**: Two routing modules - `AppRoutingModule` (main routes) and `app-routing.module.ts` (detailed routes)
- **State Management**: Service-based with RxJS Subjects for reactive state
- **Auth**: `AuthService` manages JWT tokens, role-based access, auto-authentication via localStorage
- **HTTP**: `AuthInterceptor` attaches Bearer tokens to API requests

**Key Frontend Directories:**
- `src/app/mainwindow/` - Feature components organized by functionality
- `src/app/auth/` - Authentication components, guards, services
- `src/app/header/` - Header, taskbar, user details components
- `src/app/sidemenu/` - Navigation menu with dynamic menu items

### Backend (Express/Node.js)
- **Server Entry**: `backend/server.js` (port 3000) + `backend/app.js` (Express app)
- **Database**: MongoDB with Mongoose ODM (connection in `backend/app.js`)
- **API Routes** (RESTful):
  - `/api/supplier` - Supplier CRUD
  - `/api/inventory` - Inventory/drug management
  - `/api/user` - Pharmacy staff authentication & management
  - `/api/sales` - Sales transactions
  - `/api/doctorUser` - Doctor accounts
  - `/api/doctorOder`, `/api/verifiedDoctorOder`, `/api/pickedUpOders` - Order workflow

**Middleware:**
- `backend/middleware/` - Custom middleware (auth, file upload)
- Static file serving: `/images` route serves uploaded images

### Data Models (Mongoose)
- `User` - Pharmacy staff (name, contact, NIC, email, password, role)
- `DoctorUser` - Doctor accounts
- `Inventory` - Drug inventory (email, name, quantity, batchId, expireDate, price, imagePath)
- `Supplier` - Supplier information
- `Sales` - Sales transactions
- `DoctorOder`, `VerifiedDoctorOder`, `PickedUpOders` - Multi-stage order pipeline

## Development Notes

- Frontend API calls target `http://localhost:3000` (hardcoded in services)
- JWT auth uses localStorage with automatic token refresh timer
- Role-based routes protected by `AuthGuard` (e.g., predictionreport, salesreport)
- Charts use `ng2-charts` (Chart.js wrapper) and `angular-google-charts`
- Material Design UI via `@angular/material` components
- Production MongoDB connection string in `backend/app.js` (uses MongoDB Atlas)

## Dependencies of Note

- **AI/ML**: TensorFlow.js, Brain.js for prediction charts
- **Charts**: Chart.js, ng2-charts, angular-google-charts, Chartist
- **Real-time**: Socket.io server and client
- **Email**: Nodemailer for expiry notifications
- **File Upload**: Multer for image uploads
- **Auth**: bcrypt for passwords, jsonwebtoken for tokens