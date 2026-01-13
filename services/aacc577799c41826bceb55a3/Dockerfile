FROM node:20-alpine

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9.14.4 --activate

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package.json pnpm-workspace.yaml ./

# Install dependencies (allow no frozen lockfile for fresh setups)
RUN pnpm install --no-frozen-lockfile

# Copy scripts directory
COPY scripts/ ./scripts/

# Copy the rest of the source code
COPY . .

# Create a simple HTTP server to serve the repository
RUN echo 'const http = require("http"); \
const server = http.createServer((req, res) => { \
  res.writeHead(200, {"Content-Type": "text/plain"}); \
  res.end("DefinitelyTyped Repository\\n\
This repository contains high-quality TypeScript type definitions.\\n\
Total packages: 8000+\\n\
Accessible at: https://github.com/DefinitelyTyped/DefinitelyTyped\\n"); \
}); \
const PORT = process.env.PORT || 41464; \
server.listen(PORT, "0.0.0.0", () => { \
  console.log(`Server running on port ${PORT}`); \
});' > server.cjs

# Expose port
EXPOSE 41464

# Start the server
CMD ["node", "server.cjs"]