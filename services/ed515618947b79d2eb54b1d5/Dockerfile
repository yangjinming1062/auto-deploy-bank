# Builder stage - install all deps and build
FROM node:20-alpine AS builder

WORKDIR /actionhero

# Copy package files and install all dependencies (including dev)
COPY package*.json ./
RUN npm install --ignore-scripts

# Copy source and build
COPY . .
RUN rm -rf dist && ./node_modules/.bin/tsc --sourceMap false --declaration

# Production stage
FROM node:20-alpine

ENV NODE_ENV=production
ENV PORT=8080

WORKDIR /actionhero

# Copy production package files
COPY package*.json ./
# Install production dependencies only (no dev, no scripts)
RUN npm ci --omit=dev --ignore-scripts

# Copy built artifacts from builder
COPY --from=builder /actionhero/dist ./dist
COPY --from=builder /actionhero/client ./client
COPY --from=builder /actionhero/public ./public

CMD ["node", "./dist/server.js"]
EXPOSE $PORT