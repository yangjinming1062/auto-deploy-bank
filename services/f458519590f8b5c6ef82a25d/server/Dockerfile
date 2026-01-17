# Use Node.js 20 as the base image
FROM node:20-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d

# Install pnpm globally
RUN npm install -g pnpm

# Copy package.json and pnpm-lock.yaml for dependency caching
COPY package*.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Install root dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application
COPY . .

# Build toolkit and server packages (skip client due to TypeScript dependency issues)
WORKDIR /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d/toolkit
# Fix the @types/node version incompatibility by installing a compatible version
RUN npm install --no-save @types/node@14.18.0
# Build toolkit with skipLibCheck
RUN node ../node_modules/typescript/bin/tsc --skipLibCheck && cp -r src/locales dist/

WORKDIR /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d/server
# Install server dependencies
RUN pnpm install --frozen-lockfile
# Build server
RUN pnpm run build

# Expose port
EXPOSE 3002

# Set NODE_ENV and PORT environment variables
ENV NODE_ENV=production
ENV PORT=3002

# Create a non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nestjs -u 1001

# Change ownership of the app directory
RUN chown -R nestjs:nodejs /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d
USER nestjs

# Start the server application
WORKDIR /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d/server
CMD ["pnpm", "run", "start"]