# Production stage - copy pre-built artifacts
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./

# Install all dependencies (including dev for workspace packages)
RUN yarn install --frozen-lockfile --ignore-scripts && \
    # Install runtime dependency directly (bypass workspace check)
    yarn add fastest-levenshtein@1.0.16 --ignore-workspace-root-check --ignore-scripts

# Copy pre-built zxcvbn-ts core library
COPY packages/libraries/main/dist ./node_modules/@zxcvbn-ts/core/dist
COPY packages/libraries/main/package.json ./node_modules/@zxcvbn-ts/core/package.json

# Copy server file
COPY server.js ./

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the service port
EXPOSE 3000

# Run the server
CMD ["node", "server.js"]