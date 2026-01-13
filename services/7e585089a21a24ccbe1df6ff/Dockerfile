# Build stage
FROM node:20-alpine AS builder

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Set working directory
WORKDIR /app

# Copy root package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies at root
RUN pnpm install --frozen-lockfile

# Copy entire project
COPY . .

# Build the project (including all packages and test apps)
ENV CI=true
RUN pnpm build

# Production stage
FROM node:20-alpine

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV PORT=4000
ENV CI=true

# Copy package files and lock file
COPY package.json pnpm-lock.yaml ./

# Install root dependencies
RUN pnpm install --frozen-lockfile --prod

# Copy built application and all dependencies from builder stage
COPY --from=builder /app/js ./js

# Expose the internal port
EXPOSE 4000

# Start the Express test app
CMD ["node", "js/testapps/express/lib/index.js"]
