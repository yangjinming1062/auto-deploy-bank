# Multi-stage build for React-admin monorepo
FROM node:20-alpine AS builder

# Install dependencies
WORKDIR /app

# Copy yarn lockfile, configuration, and .yarn directory (needed for Yarn 4)
COPY yarn.lock ./
COPY .yarnrc.yml ./
COPY .yarn/ ./.yarn/
COPY package.json ./

# Install all dependencies
RUN yarn install

# Development stage - run the simple example
FROM node:20-alpine AS development

WORKDIR /app

# Copy yarn lockfile, configuration, .yarn directory, and package.json
COPY yarn.lock ./
COPY .yarnrc.yml ./
COPY .yarn/ ./.yarn/
COPY package.json ./

# Install dependencies
RUN yarn install

# Copy the entire monorepo (needed for linking local packages)
COPY . .

# Install simple example specific dependencies (including vite)
WORKDIR /app/examples/simple
RUN yarn install

# Set working directory back to app root
WORKDIR /app

# Set environment variables
ENV NODE_ENV=development
ENV PORT=8080
ENV HOST=0.0.0.0

# Expose port 8080
EXPOSE 8080

# Run the simple example in development mode
# Using cd to ensure we're in the right directory and bind to all interfaces
CMD ["sh", "-c", "cd examples/simple && yarn dev --host 0.0.0.0"]