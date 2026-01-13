# Dockerfile for Reaction Commerce API
FROM node:20-alpine

# Install dependencies needed for pnpm and git
RUN apk add --no-cache \
    git \
    curl \
    bash \
    shadow

# Install pnpm
RUN npm install -g pnpm@8.15.1

# Set shell for pnpm
ENV SHELL=/bin/bash

WORKDIR /usr/local/src/app

# Copy workspace configuration
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Copy packages before install so pnpm can link them
COPY packages ./packages
COPY apps ./apps

# Install dependencies (pnpm will link workspace packages)
RUN pnpm install --no-frozen-lockfile

# Create non-root user and required directories
RUN addgroup -g 1001 nodejs && \
    adduser -u 1001 -G nodejs -D -h /home/reaction -s /bin/bash reaction && \
    mkdir -p /usr/local/src/app/uploads /usr/local/src/app/public && \
    chown -R reaction:nodejs /usr/local/src/app/uploads /usr/local/src/app/public

USER reaction

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Use tini to handle signals properly (tini is already installed in node:20-alpine)
CMD ["node", "./apps/reaction/src/index.js"]
