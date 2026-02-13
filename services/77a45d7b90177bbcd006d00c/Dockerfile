FROM node:20-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Copy tsconfig base for extends resolution
COPY tsconfig*.json ./

# Install dependencies (including dev for postinstall patch-package)
RUN npm ci

# Install wrangler globally for workerd binary
RUN npm install -g wrangler

# Copy workspace packages source
COPY packages ./packages

# Install workspace dependencies (links packages)
RUN npm install

# Build workspace packages needed by agents example
RUN npm run build -w packages/agents

# Create a simple worker that demonstrates the agents package
RUN mkdir -p /app/simple-worker/src
RUN echo 'export default { async fetch(request, env, ctx) { return new Response("Cloudflare Agents Worker is running! Agents Package available. Environment: " + process.env.NODE_ENV, { headers: { "Content-Type": "text/plain" } }); } };' > /app/simple-worker/src/index.ts

# Copy wrangler.jsonc for simple worker configuration
RUN echo '{"name": "simple-agent-worker", "main": "src/index.ts", "compatibility_date": "2026-01-28", "compatibility_flags": ["nodejs_compat"]}' > /app/simple-worker/wrangler.jsonc

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Set environment variables
ENV NODE_ENV=production
ENV EMAIL_SECRET=demo-secret-change-in-production

# Expose the wrangler dev server port
EXPOSE 8787

# Run the startup script
CMD ["/app/start.sh"]