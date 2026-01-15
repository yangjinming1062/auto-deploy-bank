# FlyFish Application - Root Dockerfile
# Builds the lcapServer component

FROM node:20-alpine AS builder

WORKDIR /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf

# Copy lcapServer package files
COPY lcapServer/package*.json ./lcapServer/

# Install dependencies for lcapServer
RUN cd lcapServer && npm install --omit=dev

# Copy application code
COPY lcapServer/ ./lcapServer/

# Create necessary directories
RUN mkdir -p lcapServer/logs lcapServer/www lcapServer/home/ubuntu/deploy-projects/761e5623bd8b94717cba3dafData

# Final stage
FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf

# Copy from builder
COPY --from=builder /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer

# Set environment variables
ENV NODE_ENV=production
ENV PORT=7001
ENV EGG_SERVER_ENV=prod
ENV WORKERS=1

# Install tini for proper process management
RUN apk add --no-cache tini

# Create necessary directories
RUN mkdir -p /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer/logs \
             /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer/www \
             /home/ubuntu/deploy-projects/761e5623bd8b94717cba3daf/lcapServer/home/ubuntu/deploy-projects/761e5623bd8b94717cba3dafData

# Expose internal port
EXPOSE 7001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:7001/users/info || exit 1

# Start the application using tini for proper signal handling
COPY start-app.sh /usr/local/bin/start-app.sh
RUN chmod +x /usr/local/bin/start-app.sh
CMD ["tini", "--", "/usr/local/bin/start-app.sh"]