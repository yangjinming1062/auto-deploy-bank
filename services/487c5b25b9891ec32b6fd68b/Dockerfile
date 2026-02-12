# syntax=docker/dockerfile:1

# Build stage for authentik web components
FROM --platform=${BUILDPLATFORM} node:20-alpine AS node-builder

ARG GIT_BUILD_HASH
ENV GIT_BUILD_HASH=${GIT_BUILD_HASH}
ENV NODE_ENV=production

WORKDIR /work/web

# Copy package files and install dependencies
COPY web/package*.json ./
COPY web/packages/sfe/package.json ./packages/sfe/ 2>/dev/null || true
COPY web/scripts ./scripts

RUN npm ci --only=production

# Copy source files
COPY web/src ./src
COPY web/authentik ./authentik
COPY web/icons ./icons
COPY web/fonts ./fonts

# Copy root package.json for workspaces
COPY package*.json ./

# Build the web UI
RUN npm run build

# Production stage - serve static files
FROM nginx:alpine AS production

COPY --from=node-builder /work/web/dist/ /usr/share/nginx/html/
COPY --from=node-builder /work/web/robots.txt /usr/share/nginx/html/robots.txt
COPY --from=node-builder /work/web/security.txt /usr/share/nginx/html/security.txt

# Expose the web port
EXPOSE 9000

CMD ["nginx", "-g", "daemon off;"]