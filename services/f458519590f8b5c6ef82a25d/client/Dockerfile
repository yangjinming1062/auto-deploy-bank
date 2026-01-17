# Use Node.js 20 as the base image
FROM node:20-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d

# Install pnpm globally
RUN npm install -g pnpm

# Copy package.json and pnpm-lock.yaml for dependency caching
COPY package*.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application
COPY . .

# Build the client application
WORKDIR /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d/client
RUN pnpm run build

# Expose port
EXPOSE 3001

# Set NODE_ENV and PORT environment variables
ENV NODE_ENV=production
ENV PORT=3001

# Create a non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership of the app directory
RUN chown -R nextjs:nodejs /home/ubuntu/deploy-projects/f458519590f8b5c6ef82a25d
USER nextjs

# Start the application
CMD ["pnpm", "run", "start"]