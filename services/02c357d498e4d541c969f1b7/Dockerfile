FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/02c357d498e4d541c969f1b7

# Install build tools for native modules
RUN apk add --no-cache python3 make g++

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application files
COPY . .

# Create a mock natives module for Node.js 20 compatibility (old graceful-fs 3.x requires it)
RUN rm -rf node_modules/natives && \
    mkdir -p node_modules/natives && \
    cat > node_modules/natives/index.js << 'EOF'
// Mock natives module for Node.js 20+ compatibility
var natives = {};
exports.source = function(id) { return natives[id] || ''; };
exports.require = function(id, whitelist) {
  if (id === 'fs') {
    return require('fs');
  }
  if (id === 'stream') {
    return require('stream');
  }
  return {};
};
EOF

# Use Docker-compatible files (memory session store instead of Redis)
RUN cp app.js.docker app.js || true
RUN cp util/redis.js.docker util/redis.js || true
RUN cp bin/www.docker bin/www || true

# Create upload directory
RUN mkdir -p public/upload

# Expose internal port
EXPOSE 81

# Set environment variables
ENV NODE_ENV=production
ENV PORT=81

# Run startup script
CMD ["sh", "start.sh"]