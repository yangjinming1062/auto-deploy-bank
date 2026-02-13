FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/164e5505886d3fd2dd221c18

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy package files and install all dependencies (needed for build)
COPY package*.json ./
RUN npm ci

# Copy source code and build the project
COPY . .
RUN npm run build && npm run gulp LKG

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the service port
EXPOSE 3000

# Run the server
CMD ["node", "server.js"]