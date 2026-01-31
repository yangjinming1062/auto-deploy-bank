FROM node:20-alpine

# Install pnpm and wget for healthcheck
RUN npm install -g pnpm@10.13.1 && apk add --no-cache wget

WORKDIR /home/ubuntu/deploy-projects/e1145ae9acf3e83e1f741985

# Copy entire workspace first (required for workspace:* dependencies)
COPY . .

# Install dependencies
RUN pnpm install --no-frozen-lockfile

# Build the monorepo
RUN pnpm run prepare-build

# Create a simple health check server
RUN echo 'const http = require("http"); \
const server = http.createServer((req, res) => { \
  res.writeHead(200, { "Content-Type": "application/json" }); \
  res.end(JSON.stringify({ status: "ok", message: "Modern.js framework built successfully" })); \
}); \
server.listen(process.env.PORT || 8080, "0.0.0.0", () => { \
  console.log("Server running on port " + (process.env.PORT || 8080)); \
});' > /home/ubuntu/deploy-projects/e1145ae9acf3e83e1f741985/server.js

ENV NODE_ENV=production
ENV PORT=8080

EXPOSE 8080

CMD ["node", "server.js"]