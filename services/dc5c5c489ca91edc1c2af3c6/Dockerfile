# Build stage
FROM node:20-alpine AS builder

WORKDIR /home/ubuntu/deploy-projects/dc5c5c489ca91edc1c2af3c6

# NOTE: Don't set NODE_ENV=production here, as it prevents devDependencies from being installed

# Create fake husky script to prevent prepare script from failing
RUN mkdir -p /usr/local/bin
RUN cat > /usr/local/bin/husky << 'HUSKY_SCRIPT'
#!/bin/sh
exit 0
HUSKY_SCRIPT
RUN chmod +x /usr/local/bin/husky

# Copy package files and install dependencies
COPY package*.json ./

RUN npm install

# Copy source code
COPY . .

# Build the project
RUN npm run build

# Create index.html for preview server with importmap to resolve React
RUN echo '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Simulacrum</title><link rel="stylesheet" href="/style.css"><script>window.process = { env: { NODE_ENV: "production" } };</script><script type="importmap">{"imports":{"react":"https://esm.sh/react@18.2.0","react-dom":"https://esm.sh/react-dom@18.2.0"}}</script></head><body><div id="root"><h1>Simulacrum Library</h1><p>Bundle: dist/index.js</p><p>Types: dist/index.d.ts</p></div><script type="module" src="/index.js"></script></body></html>' > dist/index.html

# Production stage
FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/dc5c5c489ca91edc1c2af3c6

ENV NODE_ENV=production
ENV PORT=5173

# Copy built assets from builder
COPY --from=builder /home/ubuntu/deploy-projects/dc5c5c489ca91edc1c2af3c6/dist ./dist

# Expose the port
EXPOSE 5173

# For library projects, use vite preview to serve the built files
CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "5173"]