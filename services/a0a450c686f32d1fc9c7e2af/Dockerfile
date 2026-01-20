FROM node:20-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/a0a450c686f32d1fc9c7e2af

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (including dev) but skip lifecycle hooks
RUN npm ci --ignore-scripts

# Copy source code
COPY . .

# Build the library (transpile src to root)
RUN ./node_modules/.bin/babel src --out-dir ./

# Expose the port
EXPOSE 3000

# Start the server
CMD ["node", "server.js"]