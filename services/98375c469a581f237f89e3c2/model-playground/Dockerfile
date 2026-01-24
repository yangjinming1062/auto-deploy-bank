# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
ENV NODE_OPTIONS="--openssl-legacy-provider"
ENV PATH=/app/node_modules/.bin:$PATH

# Copy package files first for better layer caching
COPY package*.json ./

# Install dependencies
RUN yarn install --frozen-lockfile 2>/dev/null || yarn install

# Copy source code
COPY . .

# Build using local Angular CLI via node_modules/.bin/ng
RUN node_modules/.bin/ng build --configuration production

# Production stage
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]