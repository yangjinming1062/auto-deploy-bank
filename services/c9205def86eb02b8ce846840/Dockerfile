# Build stage
FROM node:20-alpine AS builder

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /home/ubuntu/deploy-projects/c9205def86eb02b8ce846840

# Copy package files
COPY pnpm-lock.yaml pnpm-workspace.yaml ./
COPY patches/ patches/
COPY site/package.json site/package.json

# Install dependencies (allow new deps from package.json)
RUN pnpm install --filter wener-website

# Copy source code
COPY . .

# Build TypeScript plugins
RUN cd site && pnpm exec tsc -p tsconfig.build.json

# Build the site
RUN pnpm --filter wener-website run build

# Production stage - using nginx to serve static files
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /home/ubuntu/deploy-projects/c9205def86eb02b8ce846840/site/build /usr/share/nginx/html

# Copy nginx configuration
COPY <<'EOF' /etc/nginx/conf.d/default.conf
server {
    listen 3000;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Handle SPA routing - redirect to index.html for non-file paths
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]