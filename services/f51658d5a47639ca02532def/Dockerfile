FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/f51658d5a47639ca02532def

# Install git for npm dependencies that may require it
RUN apk add --no-cache git python3 make g++

# Copy package files
COPY package*.json ./

# Copy bower.json early (needed for postinstall)
COPY bower.json ./

# Install production dependencies without running postinstall scripts
RUN npm install --production --legacy-peer-deps --ignore-scripts && \
    npm install -g bower --legacy-peer-deps

# Copy application files
COPY . .

# Run setup tasks that postinstall would do (without --allow-root issue)
RUN cp config/env/development.json5.sample config/env/development.json5 && \
    cp config/env/production.json5.sample config/env/production.json5 && \
    bower --allow-root -f install && \
    node node_modules/grunt-cli/bin/grunt copy

# Expose the internal port
EXPOSE 5555

# Set environment variables
ENV NODE_ENV=production
ENV PORT=5555

# Start the application
CMD ["node", "pm2-main.js"]