# Stage 1: Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Generate icons (required for build)
RUN yarn icon

# Build hooks with specified environment variables
ENV NODE_ENV=production
ENV NODE_OPTIONS=--openssl-legacy-provider
ENV BUILD_TYPE=hooks
ENV BUILD_ENV_MODE=production
ENV BUILD_ENV_DIST_FILENAME_JS=index.min.js
ENV BUILD_ENV_DIST_FILENAME_CSS=index.min.css

# Build es module first (required by hooks)
RUN yarn build:es

# Build hooks dist output
RUN cd hooks && yarn build:dist

# Stage 2: Production stage
FROM nginx:alpine

# Copy built artifacts from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]