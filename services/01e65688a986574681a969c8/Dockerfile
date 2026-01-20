FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install system dependencies for ffmpeg, build tools, git, and healthcheck
RUN apk add --no-cache ffmpeg python3 make g++ git wget curl bash

# Copy package files first for better layer caching
COPY package*.json ./

# Install dependencies
RUN npm install --omit=dev && npm install -g pm2

# Copy application source
COPY . .

# Create required directories
RUN mkdir -p logs

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV NODE_ENV=production
ENV PORT=9090

# Expose the port the app listens on
EXPOSE 9090

# Health check based on PM2 status
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD pm2 list | grep -q "SHABAN-MD" && pm2 jlist | grep -q '"status":"online"' || exit 1

# Start the app with custom entrypoint
CMD ["./entrypoint.sh"]