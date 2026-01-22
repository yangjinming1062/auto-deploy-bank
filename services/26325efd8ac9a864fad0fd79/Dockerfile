# Build stage - includes Java for Leiningen/ClojureScript compilation
FROM eclipse-temurin:8-jdk-alpine AS builder

# Install Node.js and build dependencies
RUN apk add --no-cache nodejs npm python3 make g++ bash

# Install Leiningen
RUN LEIN_VERSION=2.11.2 && \
    wget -q https://raw.githubusercontent.com/technomancy/leiningen/$LEIN_VERSION/bin/lein && \
    chmod +x lein && \
    mv lein /usr/local/bin/lein

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install && npm install -g grunt-cli

# Copy project configuration
COPY project.clj ./
COPY Gruntfile.js ./
COPY config.json ./

# Copy source files
COPY src ./src
COPY externs ./externs
COPY public ./public

# Build ClojureScript (server.js and client JS)
RUN lein clean && lein cljsbuild once

# Build LESS CSS
RUN grunt

# Production stage - minimal Node.js image
FROM node:20-alpine

WORKDIR /app

# Copy built artifacts from builder
COPY --from=builder /app/server.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/config.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Set environment variables
ENV NODE_ENV=production
ENV PORT=1984

# Expose internal port
EXPOSE 1984

# Run the server
CMD ["node", "server.js"]