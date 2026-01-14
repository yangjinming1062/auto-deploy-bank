# Use Node.js 20 Alpine as base image
FROM node:20-alpine

# Install git and required tools
RUN apk add --no-cache git

# Set working directory
WORKDIR /app

# Enable corepack for yarn v4
RUN corepack enable

# Copy package files first for better layer caching
COPY package*.json .yarnrc.yml ./

# Copy root-level configuration files
COPY .yarnrc.yml ./

# Copy all files
COPY . .

# Remove gitpkg dependencies that require payment
RUN node -e " \
  const pkg = JSON.parse(require('fs').readFileSync('/app/circuits/package.json', 'utf8')); \
  delete pkg.dependencies['@zk-kit/binary-merkle-root.circom']; \
  delete pkg.dependencies['anon-aadhaar-circuits']; \
  require('fs').writeFileSync('/app/circuits/package.json', JSON.stringify(pkg, null, 2)); \
"

# Configure yarn v4 with node-modules mode
RUN echo "nodeLinker: node-modules" > .yarnrc.yml && \
    echo "nmHoistingLimits: workspaces" >> .yarnrc.yml && \
    echo "enableGlobalCache: true" >> .yarnrc.yml && \
    echo "enableScripts: false" >> .yarnrc.yml && \
    echo "checksumBehavior: ignore" >> .yarnrc.yml

# Install dependencies with refresh-lockfile to update lockfile format
RUN yarn install --refresh-lockfile

# Install additional dependencies needed for web build
RUN yarn add lottie-react lottie-react-native process stream-browserify browserify-zlib util

# Build common package
RUN cd /app/common && yarn build

# Build mobile-sdk-alpha package
RUN cd /app/packages/mobile-sdk-alpha && yarn build:ts-only

# Build web app
RUN cd /app/app && npx vite build

# Expose port
EXPOSE 5173

ENV NODE_ENV=production
ENV PORT=5173

# Serve the built static files using vite preview from the dist directory
CMD ["/bin/sh", "-c", "cd /app/app/web/dist && npx vite preview --port 5173 --host"]