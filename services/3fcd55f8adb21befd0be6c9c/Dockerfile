FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./
COPY packages/_server/package.json packages/_server/package.json
COPY packages/__utils/package.json packages/__utils/package.json
COPY packages/json-rpc-api/package.json packages/json-rpc-api/package.json
COPY packages/utils-disposables/package.json packages/utils-disposables/package.json
COPY packages/utils-logger/package.json packages/utils-logger/package.json

# Install root dependencies
RUN npm ci --ignore-scripts

# Copy source code
COPY . .

# Build workspace packages
WORKDIR /app/packages/__utils
RUN npm run build

WORKDIR /app/packages/utils-disposables
RUN npm run build

WORKDIR /app/packages/utils-logger
RUN npm run build

WORKDIR /app/packages/json-rpc-api
RUN npm run build

# Build the server package (skip schema generation as it requires additional dependencies)
WORKDIR /app/packages/_server
RUN npm run clean && npx tsdown --production --minify

# Copy the pre-existing schema file from the source directory
COPY packages/_server/spell-checker-config.schema.json ./

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy built files from builder
COPY --from=builder /app/packages/_server/dist ./dist
COPY --from=builder /app/packages/_server/out ./out
COPY --from=builder /app/packages/_server/spell-checker-config.schema.json ./

# Copy package.json for main entry point
COPY --from=builder /app/packages/_server/package.json ./

# Copy internal workspace packages
COPY --from=builder /app/packages/__utils ./node_modules/@internal/common-utils
COPY --from=builder /app/packages/utils-disposables ./node_modules/utils-disposables
COPY --from=builder /app/packages/utils-logger ./node_modules/utils-logger
COPY --from=builder /app/packages/json-rpc-api ./node_modules/json-rpc-api

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV HTTP_MODE=true

# Expose the service port
EXPOSE 3000

# Use node to run the server directly
CMD ["node", "dist/main.js"]