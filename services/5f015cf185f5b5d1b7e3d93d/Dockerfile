FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/5f015cf185f5b5d1b7e3d93d

# Install Python and build tools for node-gyp
RUN apk add --no-cache python3 make g++ build-base

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build && npm run build-demo

# Install serve for static file serving
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Serve the demo application
CMD ["serve", "-s", "dist", "-l", "3000"]