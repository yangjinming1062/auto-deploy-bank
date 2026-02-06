# Stage 1: Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY docs/package*.json ./docs/
COPY yarn.lock ./

# Install dependencies for root and docs
RUN yarn install --frozen-lockfile

# Copy the rest of the project
COPY . .

# Run yarn set to set up the monorepo workspace structure
RUN yarn run set

# Build all monorepo packages
RUN yarn build

# Build the documentation site
RUN yarn run build-docs

# Stage 2: Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Install nginx first (creates /etc/nginx/http.d directory)
RUN apk add --no-cache nginx

# Copy built documentation from builder
COPY --from=builder /app/docs/dist/nlux /app/dist

# Create nginx config for serving static files with baseUrl /nlux
# Note: use http.d because conf.d is included in root context (not http block)
RUN rm -f /etc/nginx/conf.d/default.conf && \
    cat > /etc/nginx/http.d/default.conf << 'EOF'
server {
    listen 80;
    server_name localhost;
    root /app/dist;
    index index.html;

    # Redirect root to /nlux/
    location = / {
        return 302 /nlux;
    }

    location /nlux {
        alias /app/dist;
        try_files $uri $uri/ /nlux/index.html;
    }

    # Redirect /nlux requests without trailing slash
    location ~ ^/nlux$ {
        return 302 /nlux/;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Expose internal port 80
EXPOSE 80

# Set environment variables
ENV NODE_ENV=production
ENV PORT=80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/nlux/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]