FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da

# Install build dependencies
RUN apk add --no-cache python3 make g++ libc6-compat curl

# Copy package files from root (for version sync)
COPY package*.json ./

# Copy common directory (shared modules)
COPY common ./common

# Copy web directory (needed for logo.png and web build)
COPY web ./web

# Copy README.md
COPY README.md ./

# Copy electron package files
COPY electron/package*.json ./electron/
COPY electron/tsconfig.json ./electron/

# Copy types to electron directory
COPY electron/types ./electron/types

# Install all dependencies
WORKDIR /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron
RUN npm ci

# Copy source code
COPY electron/ts ./ts
COPY electron/task.mts ./
COPY electron/webpack.no_electron.js ./
COPY electron/README.md ./

# Copy common directory to electron for relative imports
# From /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron/ts/*, ../../common resolves to /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/common
RUN cp -r /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/common ./common

# Build TypeScript
RUN npm run build:node

# Return to app directory and set permissions
WORKDIR /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da
RUN chown -R node:node /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron

USER node

# Set environment variables
ENV NODE_ENV=production
ENV PORT=16100
ENV myEnv=prod
ENV runtime=node
ENV no_electron=1

# Expose the HTTP port
EXPOSE 16100

# Start the node server
WORKDIR /home/ubuntu/deploy-projects/2ae75e0d8e092bbb4e2989da/electron
CMD ["node", "js/main_no_electron.js"]
