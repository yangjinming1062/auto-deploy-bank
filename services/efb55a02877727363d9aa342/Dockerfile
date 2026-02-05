FROM node:20-alpine

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++ && npm install -g http-server

WORKDIR /home/ubuntu/deploy-projects/efb55a02877727363d9aa342

# Copy package files and install dependencies
COPY package*.json ./
# Install production deps (skip native builds)
RUN npm ci --ignore-scripts --omit=dev
# Install Electron devDependency to get binary for build
RUN npm install electron --no-save --ignore-scripts
# Download Electron binary
RUN node node_modules/electron/install.js

# Copy source files
COPY . .

# Build the Next.js static export (skip tests since Electron can't run in container)
RUN npx next build renderer && npx next export renderer

# Expose the port Next.js will run on
EXPOSE 3000

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Serve the static export
CMD ["http-server", "renderer/out", "-p", "3000", "-c-1"]