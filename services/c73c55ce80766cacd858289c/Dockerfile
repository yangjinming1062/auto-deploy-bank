# Use node:20-alpine as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
ENV PORT=4321
ENV HOST=0.0.0.0

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files and install dependencies
COPY package.json pnpm-lock.yaml* ./

# Install dependencies (including dev dependencies for build)
RUN pnpm install --frozen-lockfile

# Install missing runtime dependencies required by source code
RUN pnpm add zod github-slugger

# Copy source code
COPY . .

# Expose the port Astro runs on
EXPOSE 4321

# Start the dev server with explicit host binding
CMD ["npx", "astro", "dev", "--host", "0.0.0.0", "--port", "4321"]