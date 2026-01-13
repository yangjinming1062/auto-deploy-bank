# Dockerfile for Victory React Component Library

FROM node:20-alpine

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9.13.0 --activate

WORKDIR /app

# Copy package management files and patches
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY patches/ ./patches/
COPY packages/victory-core/package.json ./packages/victory-core/
COPY packages/victory-vendor/package.json ./packages/victory-vendor/

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build all packages in ESM format (needed for documentation)
RUN pnpm run build:lib:esm

# Install website dependencies properly in website directory
# First ensure victory packages are built
RUN cd /app/website && pnpm install --frozen-lockfile

# Ensure website can access built packages
# Create symlinks for built packages in website node_modules
RUN mkdir -p /app/website/node_modules && \
    ln -sf /app/packages/victory-core /app/website/node_modules/victory-core && \
    ln -sf /app/packages/victory /app/website/node_modules/victory

# Install a simple static file server
RUN npm install -g serve

# Set environment variables
ENV NODE_ENV=production
ENV PORT=5855

# Expose port 5855 for the documentation website
EXPOSE 5855

# Start the documentation website
# Use docusaurus from website's node_modules, bind to all interfaces
CMD ["sh", "-c", "cd /app/website && /app/website/node_modules/.bin/docusaurus start --port 5855 --host 0.0.0.0 --no-open"]