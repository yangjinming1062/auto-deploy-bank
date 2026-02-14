# ------------------------------
# Base
# ------------------------------
# Base stage: Contains only the minimal dependencies required for runtime
# (node_modules and Playwright system dependencies)
FROM node:20-alpine AS base

# Set the working directory
WORKDIR /app

RUN --mount=type=cache,target=/root/.npm,sharing=locked,id=npm-cache \
    --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=bind,source=packages/playwright-mcp/package.json,target=packages/playwright-mcp/package.json \
    npm ci --omit=dev && \
    # Install system dependencies for playwright on Alpine
    apk add --no-cache \
        chromium \
        nss \
        freetype \
        harfbuzz \
        ca-certificates \
        ttf-freefont

# ------------------------------
# Runtime
# ------------------------------
FROM base

ENV NODE_ENV=production
ENV PORT=8080
ENV PLAYWRIGHT_MCP_OUTPUT_DIR=/tmp/playwright-output

# Set the correct ownership for the runtime user on production `node_modules`
# The 'node' user already exists in node:20-alpine
RUN chown -R node:node /app

USER node

COPY --chown=node:node packages/playwright-mcp/cli.js packages/playwright-mcp/package.json ./

# Expose the HTTP/SSE port
EXPOSE 8080

# Run in headless and only with chromium (other browsers need more dependencies not included in this image)
# Arguments are passed via docker-compose command
ENTRYPOINT ["node", "cli.js"]