# Multi-stage build for AngularJS BlurAdmin application
FROM node:20-alpine AS builder

# Install system dependencies for building native modules
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    git \
    build-base

# Install dependencies
WORKDIR /app

# Copy package files
COPY package.json bower.json ./

# Install npm dependencies
RUN npm install

# Copy source code
COPY src ./src
COPY gulpfile.js ./gulpfile.js
COPY gulp ./gulp

# Build the application (bower needs --allow-root for Docker)
RUN export CI=true && \
    npx bower install --allow-root && \
    npx gulp build

# Production stage - serve with nginx
FROM nginx:alpine

# Install wget for health checks
RUN apk add --no-cache wget

# Copy built application to nginx
COPY --from=builder /app/release /usr/share/nginx/html

# Copy config data
COPY data /usr/share/nginx/data
COPY env-config.json /usr/share/nginx/html/env-config.json
RUN chmod 644 /usr/share/nginx/html/env-config.json

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create nginx configuration for SPA fallback
RUN cat > /etc/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy (if backend service is available - configure backend URL in environment)
    # location /api/ {
    #     proxy_pass http://backend:8080/;
    #     proxy_http_version 1.1;
    #     proxy_set_header Upgrade $http_upgrade;
    #     proxy_set_header Connection 'upgrade';
    #     proxy_set_header Host $host;
    #     proxy_set_header X-Real-IP $remote_addr;
    #     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header X-Forwarded-Proto $scheme;
    #     proxy_cache_bypass $http_upgrade;
    # }

    # Serve data directory
    location /data/ {
        alias /usr/share/nginx/data/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost/ || exit 1

# Start with entrypoint script
CMD ["/docker-entrypoint.sh"]