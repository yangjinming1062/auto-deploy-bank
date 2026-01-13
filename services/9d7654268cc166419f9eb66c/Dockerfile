# Use Node.js 20 Debian as base image for Electron compatibility
FROM node:20-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Quasar CLI globally
RUN npm install -g @quasar/cli

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for dev mode)
RUN npm ci

# Copy source code
COPY . .

# Set environment variables
ENV NODE_ENV=development

# Expose the web server port
EXPOSE 6080

# Health check - verify web server is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD sh -c "curl -f http://localhost:6080 || exit 1"

# Start Quasar dev server in web mode
CMD ["sh", "-c", \
     "echo 'Starting Quasar dev server in web mode...' && \
      quasar dev --port 6080 --host 0.0.0.0"]