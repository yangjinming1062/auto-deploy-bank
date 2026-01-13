# Multi-stage build for UmiJS application

# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Set build-time environment variables
ENV NODE_ENV=production
ENV NODE_OPTIONS=--openssl-legacy-provider

# Copy package files
COPY package*.json yarn.lock ./

# Install dependencies (including devDependencies for building)
# Postinstall will run automatically, which generates umi tmp files
RUN yarn install --legacy-peer-deps --include=dev

# Copy source code
COPY . .

# Build the project without compression to avoid CSS processing errors
RUN yarn run nocompress

# Production stage
FROM node:20-alpine

WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV NODE_OPTIONS=--openssl-legacy-provider

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/server.js ./server.js

# Copy only production dependencies and install them
COPY package*.json yarn.lock ./
RUN yarn install --legacy-peer-deps --only=production

# Expose port
EXPOSE 3000

# Start the server
CMD ["npm", "run", "server"]
