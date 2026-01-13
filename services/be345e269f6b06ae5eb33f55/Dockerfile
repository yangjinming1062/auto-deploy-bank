# LangChain.js Development Server Environment
FROM node:20-alpine

# Install pnpm and curl for healthchecks
RUN npm install -g pnpm@10.14.0 && apk add --no-cache curl

# Set working directory
WORKDIR /app

# Copy workspace configuration files first (for better caching)
COPY pnpm-workspace.yaml ./
COPY turbo.json ./
COPY package.json ./
COPY pnpm-lock.yaml ./

# Install root dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Install dependencies for all packages in the monorepo
RUN pnpm install --recursive

# Build all packages for production
RUN pnpm build

# Expose port for the development server
EXPOSE 41580

# Default command: start the development server
CMD ["node", "server.js"]