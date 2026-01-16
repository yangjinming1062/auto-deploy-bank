FROM node:20-alpine AS builder

# Install build dependencies
RUN apk add --no-cache python3 make g++ curl

WORKDIR /app

# Copy root package files for version sync
COPY package*.json ./

# Install root dependencies (needed for common module)
RUN npm ci --only=production=false

# Copy electron package files
COPY electron/package*.json ./electron/
COPY electron/tsconfig.json ./electron/

# Copy source files
COPY electron/ts ./electron/ts
COPY electron/task.mts ./electron/
COPY electron/webpack.no_electron.js ./electron/
COPY electron/README.md ./electron/
COPY common ./common
COPY web ./web
COPY README.md ./

# Build web frontend first (needs root node_modules for common module)
WORKDIR /app/web
RUN npm ci --only=production=false
RUN npm run build

# Build electron server
WORKDIR /app/electron
RUN npm ci --only=production=false
RUN npm run build:node

# Production stage
FROM node:20-alpine

RUN apk add --no-cache curl

WORKDIR /app

# Copy built files from builder
COPY --from=builder /app/electron/js ./js
COPY --from=builder /app/electron/web-build ./web-build
COPY --from=builder /app/electron/node_modules ./node_modules
COPY --from=builder /app/electron/package.json ./

# Environment variables
ENV NODE_ENV=production
ENV myEnv=prod
ENV runtime=node
ENV no_electron=1
ENV PORT=16100

EXPOSE 16100

CMD ["node", "js/main_no_electron.js"]