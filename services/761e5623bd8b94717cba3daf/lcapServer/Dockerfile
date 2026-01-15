# lcapServer Dockerfile for Egg.js FlyFish Application
FROM node:20-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer

# Set environment variables
ENV NODE_ENV=production
ENV PORT=7001
ENV EGG_SERVER_ENV=docker

# Install dependencies for node-gyp (needed for some native modules)
RUN apk add --no-cache python3 make g++ bash

# Copy package files
COPY package*.json ./

# Install dependencies (production only)
RUN npm install --only=production

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer/logs \
             /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer/www \
             /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/home/ubuntu/deploy-projects/761e5623bd8b94717cba3dafData

# Expose internal port
EXPOSE 7001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:7001/users/info || exit 1

# Start the application
CMD ["sh", "-c", "EGG_SERVER_ENV=docker npx egg-scripts start --daemon --title=egg-server-FlyFish --workers=2"]