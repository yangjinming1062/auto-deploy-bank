# Stage 1: Build stage
FROM node:20-alpine AS builder

# Install pnpm
ENV PNPM_HOME=/pnpm
ENV PATH=$PNPM_HOME/bin:$PATH
RUN corepack enable && corepack prepare pnpm@9.3.0 --activate

WORKDIR /app

# Copy root workspace configuration
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY nx.json ./

# Copy packages and apps directories
COPY packages packages
COPY apps apps

# Temporarily disable the prepare script to avoid build failure during install
RUN sed -i 's/"prepare": "simple-git-hooks && husky && pnpm run build"/"prepare": "echo skipping prepare"/' package.json

# Install dependencies
RUN pnpm install --no-frozen-lockfile

# Build the playground app
RUN pnpm run build

# Copy built artifacts
RUN mkdir -p packages/playground/static && \
    cp -r apps/playground/dist/* packages/playground/static/ 2>/dev/null || true

# Stage 2: Production stage
FROM node:20-alpine

ENV NODE_ENV=production
ENV PORT=3000

WORKDIR /app

# Install serve to serve static files
RUN npm install -g serve

# Copy built artifacts from builder
COPY --from=builder /app/packages/playground/static ./dist

# Expose the port
EXPOSE 3000

# Start the server
CMD ["serve", "-s", "dist", "-l", "3000"]