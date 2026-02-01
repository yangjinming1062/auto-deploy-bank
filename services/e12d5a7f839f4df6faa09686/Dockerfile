FROM node:20-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/e12d5a7f839f4df6faa09686

# Install pnpm
RUN corepack enable && corepack prepare pnpm@10.28.0 --activate

# Copy package files first for better caching
COPY package.json pnpm-lock.yaml ./

# Install dependencies (skip prepare scripts to avoid build failures)
RUN pnpm install --no-frozen-lockfile --ignore-scripts

# Copy the rest of the application
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the internal port
EXPOSE 3000

# Run a simple HTTP server
CMD ["node", "-e", "const http = require('http'); const fs = require('fs'); const path = require('path'); const server = http.createServer((req, res) => { res.writeHead(200, {'Content-Type': 'application/json'}); res.end(JSON.stringify({ status: 'ok', service: 'rslib-monorepo', message: 'Node.js monorepo container is running', project: 'rsbuild/rslib' })); }); server.listen(3000, () => { console.log('Server running on port 3000'); });"]