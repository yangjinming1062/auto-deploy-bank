FROM node:20-alpine AS builder

# Install git for yarn plugins
RUN apk add --no-cache git

WORKDIR /app

# Initialize git repo for yarn git hooks plugin
RUN git init && git config user.email "docker@localhost" && git config user.name "Docker"

# Copy package files
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn .yarn/
COPY packages/core/package.json packages/core/
COPY packages/react/package.json packages/react/
COPY packages/documentation/package.json packages/documentation/

# Install dependencies
RUN yarn install --immutable

# Copy source code
COPY . .

# Build core and react packages first (required for documentation)
RUN yarn build:core && yarn build:react

# Build documentation
RUN yarn build:documentation

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Install serve for static file serving
RUN npm install -g serve

# Copy built documentation from builder
COPY --from=builder /app/packages/documentation/dist ./dist

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose port
EXPOSE 3000

# Start the server
CMD ["serve", "-s", "dist", "-l", "3000"]