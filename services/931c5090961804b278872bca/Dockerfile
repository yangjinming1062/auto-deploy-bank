# Base stage
FROM node:20-alpine AS base

# Install pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@10.17.1 --activate

# Build stage - builds all packages with full dependencies
FROM base AS builder

WORKDIR /app

# Copy entire project for workspace resolution
COPY . .

# Install dependencies (including devDependencies for build)
RUN pnpm install --no-frozen-lockfile

# Build all packages
RUN pnpm build

# Production stage - minimal runtime environment
FROM base AS production

WORKDIR /app

# Copy everything from builder - includes built artifacts and node_modules
COPY --from=builder /app /app

# Create demo profile directory
RUN mkdir -p /app/.rsdoctor

# Create a minimal demo manifest
RUN echo '{"data":{"alerts":[],"chunks":[],"modules":[],"packages":[],"loaders":[],"plugins":[],"entries":[],"sources":[],"bundles":[]},"client":{"enableRoutes":["overview","bundles","modules","packages","loaders","plugins","entries","analysis","bundle-diff"]},"__LOCAL__SERVER__":true}' > /app/.rsdoctor/manifest.json

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Run the rsdoctor analyze command with demo profile
CMD ["node", "packages/cli/bin/rsdoctor", "analyze", "--profile", "/app/.rsdoctor/manifest.json", "--port", "3000", "--no-open"]