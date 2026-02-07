# Build stage
FROM node:20-alpine AS builder

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Set working directory
WORKDIR /app

# Copy package files and source code first
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY pnpm-workspace.yaml ./
COPY . .

# Install dependencies
RUN pnpm install --frozen-lockfile

# Install peer dependencies needed for type checking
RUN pnpm add -Dw webpack@5 memfs@4 @types/node@^22

# Build the project
RUN pnpm build

# Production stage
FROM node:20-alpine

# Install runtime dependencies
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy node_modules from builder (includes all dependencies and workspace links)
COPY --from=builder /app/node_modules ./node_modules

# Copy built artifacts from builder
COPY --from=builder /app/packages ./packages

# Copy e2e fixtures for sample data
COPY --from=builder /app/e2e/fixtures/rsdoctor ./e2e/fixtures/rsdoctor

# Set environment variables
ENV NODE_ENV=production
ENV PORT=2024
ENV LOCAL_CLI_PORT=2024
ENV ENABLE_CLIENT_SERVER=false
ENV DEBUG=false
ENV NO_COLOR=true

# Create volume mount point for data
VOLUME /data

# Expose the server port
EXPOSE 2024

# Set working directory to CLI
WORKDIR /app/packages/cli

# Run the CLI with sample manifest (use absolute path)
CMD ["node", "bin/rsdoctor", "analyze", "--profile", "/app/e2e/fixtures/rsdoctor/manifest.json", "--port", "2024", "--no-open"]