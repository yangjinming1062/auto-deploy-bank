# Multi-stage build for Wipi CMS monorepo

# Stage 1: Build all packages
FROM node:20-alpine AS builder

# Install latest pnpm
RUN npm install -g pnpm@latest

# Set working directory
WORKDIR /app

# Copy root package files
COPY package.json pnpm-lock.yaml ./

# Copy pnpm workspace configuration
COPY pnpm-workspace.yaml ./

# Copy all package manifests
COPY packages/server/package.json packages/server/
COPY packages/client/package.json packages/client/
COPY packages/admin/package.json packages/admin/
COPY packages/config/package.json packages/config/

# Upgrade TypeScript to 4.9.x (last 4.x version, better @types compatibility)
# Update TypeScript in root package.json and all workspace packages
RUN sed -i 's/"typescript": "\^4\.5\.5"/"typescript": "^4.9.5"/g' package.json && \
    sed -i 's/"typescript": "4\.6\.2"/"typescript": "^4.9.5"/g' packages/*/package.json && \
    sed -i 's/"typescript": "\^3\.6\.3"/"typescript": "^4.9.5"/g' packages/*/package.json && \
    sed -i 's/"typescript": "~4\.5\.5"/"typescript": "~4.9.5"/g' packages/*/package.json && \
    cat package.json | grep typescript

# Install all dependencies (without --frozen-lockfile to allow format adaptation)
RUN rm -f pnpm-lock.yaml
RUN pnpm install --no-lockfile

# Verify TypeScript version
RUN npx tsc --version

# Copy source code, environment files, and locales
COPY packages ./packages
COPY .env .env.prod ./
COPY locales ./locales
COPY locales ./packages/config/locales

# Debug: verify locales are accessible
RUN ls -la /app/locales/ && cat /app/locales/zh.json | head -3

# Build packages in order: config -> server -> client -> admin
RUN pnpm run build:config && \
    pnpm run build:server && \
    pnpm run build:client && \
    pnpm run build:admin

# Stage 2: Server service
FROM node:20-alpine AS server

# Install pnpm
RUN npm install -g pnpm@latest

WORKDIR /app

# Copy pnpm config and all package manifests for workspace
COPY pnpm-workspace.yaml ./
COPY package.json ./
COPY packages/server/package.json packages/server/
COPY packages/client/package.json packages/client/
COPY packages/admin/package.json packages/admin/
COPY packages/config/package.json packages/config/

# Install dependencies for the server package using pnpm
RUN pnpm install --no-frozen-lockfile

# Copy built server, config and env files from builder
COPY --from=builder /app/packages/server/dist ./packages/server/dist
COPY --from=builder /app/packages/config/lib ./packages/config/lib
COPY --from=builder /app/.env ./
COPY --from=builder /app/.env.prod ./

EXPOSE 3003
ENV NODE_ENV=production
ENV PORT=3003
# Run node from packages/server directory where dependencies are installed
WORKDIR /app/packages/server
CMD ["node", "dist/main"]

# Stage 3: Client service
FROM node:20-alpine AS client

# Install pnpm
RUN npm install -g pnpm@latest

WORKDIR /app

# Copy pnpm config and all package manifests for workspace
COPY pnpm-workspace.yaml ./
COPY package.json ./
COPY packages/server/package.json packages/server/
COPY packages/client/package.json packages/client/
COPY packages/admin/package.json packages/admin/
COPY packages/config/package.json packages/config/

# Install dependencies for the client package using pnpm
RUN pnpm install --no-frozen-lockfile

# Copy built client, config and env files from builder to packages/client directory
COPY --from=builder /app/packages/client/.next ./packages/client/.next
COPY --from=builder /app/packages/client/public ./packages/client/public
COPY --from=builder /app/packages/client/next.config.js ./packages/client/
COPY --from=builder /app/packages/client/next-sitemap.js ./packages/client/
COPY --from=builder /app/packages/client/prod-server.js ./packages/client/
COPY --from=builder /app/packages/config/lib ./packages/config/lib
COPY --from=builder /app/packages/config/locales ./packages/config/locales
COPY --from=builder /app/.env ./
COPY --from=builder /app/.env.prod ./
COPY --from=builder /app/locales ./locales/

EXPOSE 3001
ENV NODE_ENV=production
ENV PORT=3001
# Run node from packages/client directory where dependencies are installed
WORKDIR /app/packages/client
CMD ["node", "prod-server.js"]

# Stage 4: Admin service
FROM node:20-alpine AS admin

# Install pnpm
RUN npm install -g pnpm@latest

WORKDIR /app

# Copy pnpm config and all package manifests for workspace
COPY pnpm-workspace.yaml ./
COPY package.json ./
COPY packages/server/package.json packages/server/
COPY packages/client/package.json packages/client/
COPY packages/admin/package.json packages/admin/
COPY packages/config/package.json packages/config/

# Install dependencies for the admin package using pnpm
RUN pnpm install --no-frozen-lockfile

# Copy built admin, config and env files from builder to packages/admin directory
COPY --from=builder /app/packages/admin/.next ./packages/admin/.next
COPY --from=builder /app/packages/admin/public ./packages/admin/public
COPY --from=builder /app/packages/admin/next.config.js ./packages/admin/
COPY --from=builder /app/packages/admin/prod-server.js ./packages/admin/
COPY --from=builder /app/packages/config/lib ./packages/config/lib
COPY --from=builder /app/packages/config/locales ./packages/config/locales
COPY --from=builder /app/.env ./
COPY --from=builder /app/.env.prod ./
COPY --from=builder /app/locales ./locales/

EXPOSE 3002
ENV NODE_ENV=production
ENV PORT=3002
# Run node from packages/admin directory where dependencies are installed
WORKDIR /app/packages/admin
CMD ["node", "prod-server.js"]