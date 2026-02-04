# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install pnpm (version compatible with lockfileVersion 5.4)
RUN npm install -g pnpm@7

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile --ignore-scripts

# Copy source code
COPY . .

# Set production environment
ENV NODE_ENV=production
ENV VITE_API_BASE_URL=http://localhost:8080

# Build the application
RUN pnpm run build

# Production stage - serve with nginx
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]