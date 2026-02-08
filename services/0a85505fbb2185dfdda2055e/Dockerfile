# Builder stage - Build Angular frontend (Node 16 for Angular 8 compatibility)
FROM node:16-alpine AS builder

WORKDIR /usr/src/app

# Copy package files for build
COPY package*.json ./

# Install dependencies (skip native module builds for WebGL packages)
RUN npm ci --ignore-scripts

# Copy source code
COPY . .

# Install missing dependency for ng2-carouselamos
RUN npm install lodash.isequal --ignore-scripts

# Build Angular app
RUN npm run build

# Production stage
FROM node:20-alpine

ENV NODE_ENV=production
ENV PORT=3000

WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install production dependencies only (skip native module builds)
RUN npm ci --omit=dev --ignore-scripts

# Install bcryptjs for backend authentication
RUN npm install bcryptjs --ignore-scripts

# Copy backend source
COPY backend ./backend

# Copy Angular build from builder
COPY --from=builder /usr/src/app/dist/pro ./dist/pro

# Create images directory
RUN mkdir -p images

EXPOSE 3000

CMD ["node", "backend/server.js"]