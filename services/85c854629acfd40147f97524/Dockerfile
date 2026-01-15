# syntax=docker/dockerfile:1
FROM node:20-alpine

# Set up working directory
WORKDIR /app

# Install build dependencies (including bash for scripts)
RUN apk add --no-cache python3 make g++ curl bash

# Copy package files first for better layer caching
COPY package.json yarn.lock ./

# Copy workspace package files
COPY packages/unigraph-dev-backend/package.json packages/unigraph-dev-backend/package.json
COPY packages/unigraph-dev-common/package.json packages/unigraph-dev-common/package.json
COPY packages/unigraph-packager/package.json packages/unigraph-packager/package.json

# Install dependencies (skip all scripts to avoid native module build issues)
RUN yarn install --frozen-lockfile --ignore-scripts --network-timeout 600000 || \
    yarn install --ignore-scripts --network-timeout 600000

# Copy source code
COPY packages/unigraph-dev-backend packages/unigraph-dev-backend
COPY packages/unigraph-dev-common packages/unigraph-dev-common
COPY packages/unigraph-packager packages/unigraph-packager
COPY packages/default-packages packages/default-packages
COPY scripts scripts
COPY secrets.env.json .

# Install compatible older type definitions for TypeScript 4.2
RUN npm install --no-save --legacy-peer-deps @types/react@17 @types/react-dom@17 @types/node@14

# Build the default packages
RUN mkdir -p packages/unigraph-dev-common/lib/data && \
    for entry in packages/default-packages/*; do \
        echo "building $entry"; \
        node packages/unigraph-packager/unigraph-packager.js "$entry" -o packages/unigraph-dev-common/lib/data; \
    done

# Build the backend and common packages with skipLibCheck
RUN cd packages/unigraph-dev-common && \
    ./node_modules/.bin/tsc --skipLibCheck && \
    cd ../unigraph-dev-backend && \
    ./node_modules/.bin/tsc --skipLibCheck && \
    cp ../../secrets.env.json dist/

# Clean up build dependencies
RUN apk del python3 make g++ curl bash

# Set environment variables
ENV NODE_ENV=production
ENV PORT=4001
ENV DGRAPH_HOST=dgraph
ENV UNIGRAPH_RECOVERY_MODE=

# Expose the main internal port
EXPOSE 4001

# Start the backend server
CMD ["node", "/app/packages/unigraph-dev-backend/dist/index.js"]