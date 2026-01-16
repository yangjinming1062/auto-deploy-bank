FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron

# Install dependencies for build tools
RUN apk add --no-cache python3 make g++ libc6-compat

# Copy package files first for better caching
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the TypeScript files
RUN npm run build

# Use non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron

USER nodejs

# Set environment variables
ENV NODE_ENV=production
ENV PORT=16100

# Expose the HTTP port
EXPOSE 16100

# Start the node server
CMD ["node", "js/main_no_electron.js"]