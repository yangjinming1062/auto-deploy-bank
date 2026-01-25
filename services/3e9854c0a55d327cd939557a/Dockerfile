FROM node:14-alpine

WORKDIR /home/ubuntu/deploy-projects/3e9854c0a55d327cd939557a

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++

# Install production dependencies
COPY package*.json ./
RUN npm install --omit=dev --ignore-scripts

# Create mock pwuid module for native module compatibility
RUN mkdir -p /home/ubuntu/deploy-projects/3e9854c0a55d327cd939557a/node_modules/pwuid && \
    echo 'module.exports = function() { return { dir: "/root", pw_shell: "/bin/sh" }; };' > /home/ubuntu/deploy-projects/3e9854c0a55d327cd939557a/node_modules/pwuid/index.js

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 9000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=9000

# Run the application
CMD ["node", "pm2-web.js"]