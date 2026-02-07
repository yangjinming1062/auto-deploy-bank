FROM node:20-alpine

# Install git for build process, openssl for key generation, and native module build tools
RUN apk add --no-cache \
    git \
    make \
    g++ \
    python3 \
    openssl \
    musl-dev \
    nodejs-dev \
    libffi-dev

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/9e8c5d159fe460d2b0592105

# Copy package files first for better caching
COPY package*.json ./

# Install node dependencies
RUN npm install --legacy-peer-deps --omit=optional

# Create stub for incompatible sqlite-fts module
RUN mkdir -p /home/ubuntu/deploy-projects/9e8c5d159fe460d2b0592105/node_modules/sqlite-fts && \
    echo 'module.exports = {Database: function() {return {open: function() {}, index: function() {}, search: function() {}, insert: function() {}, delete: function() {}}};' > /home/ubuntu/deploy-projects/9e8c5d159fe460d2b0592105/node_modules/sqlite-fts/index.js

# Copy application source
COPY . .

# Ensure scripts are executable
RUN chmod +x /home/ubuntu/deploy-projects/9e8c5d159fe460d2b0592105/locker /home/ubuntu/deploy-projects/9e8c5d159fe460d2b0592105/scripts/*.sh

# Set environment variables
ENV NODE_ENV=production
ENV NODE_PATH=/home/ubuntu/deploy-projects/9e8c5d159fe460d2b0592105/Common/node
ENV PORT=8042

# Expose internal port
EXPOSE 8042

# Start the application
CMD ["node", "lockerd.js"]