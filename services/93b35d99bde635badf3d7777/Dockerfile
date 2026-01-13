# Use Node.js 20 Alpine base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files for dependency caching
COPY package.json yarn.lock ./
COPY applications/web/package.json ./applications/web/

# Install dependencies
RUN yarn install --production=false
RUN cd applications/web && yarn install --production=false

# Install next globally
RUN npm install -g next@11

# Copy source code
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV PORT=40111
ENV NODE_OPTIONS=--openssl-legacy-provider

# Expose port
EXPOSE 40111

# Start the web application in dev mode
WORKDIR /app/applications/web
CMD ["npx", "next@11", "dev"]