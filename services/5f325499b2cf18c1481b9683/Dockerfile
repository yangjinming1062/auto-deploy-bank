FROM node:20-alpine

WORKDIR /home/node/app

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (reload is required by server.js even for conditional use)
RUN npm ci

# Copy application source
COPY . .

# Build the application
RUN npm run build

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Run the server
CMD ["npm", "run", "serve"]