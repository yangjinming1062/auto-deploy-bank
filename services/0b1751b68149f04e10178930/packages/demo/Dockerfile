# Stage 1: Build the Vue CLI application
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies using yarn
COPY package*.json yarn.lock* ./
RUN yarn install --frozen-lockfile

# Copy source and build
COPY . .
RUN yarn run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]