# Stage 1: Dependencies installation
FROM node:20-alpine AS deps

WORKDIR /app

# Install global yarn
RUN corepack enable && corepack prepare yarn@1.22.22 --activate

# Copy package files first for better caching
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --non-interactive

# Copy the rest of the application
COPY . .

# Bootstrap lerna packages
RUN npx lerna bootstrap -- --legacy-peer-deps --non-interactive

# Build the required scoped packages (needed for Gatsby to work)
RUN yarn build:lib --scope @douyinfe/semi-json-viewer-core --scope @douyinfe/semi-webpack-plugin --scope eslint-plugin-semi-design || true

# Stage 2: Production image
FROM node:20-alpine AS runner

WORKDIR /app

# Copy package files and installed dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json ./package.json
COPY --from=deps /app/yarn.lock ./yarn.lock
COPY --from=deps /app/lerna.json ./lerna.json
COPY --from=deps /app/packages ./packages
COPY --from=deps /app/static ./static
COPY --from=deps /app/content ./content
COPY --from=deps /app/src ./src
COPY --from=deps /app/gatsby-config.js ./
COPY --from=deps /app/gatsby-node.js ./
COPY --from=deps /app/gatsby-browser.js ./
COPY --from=deps /app/gatsby-ssr.js ./
COPY --from=deps /app/tsconfig.json ./
COPY --from=deps /app/scripts ./scripts
COPY --from=deps /app/plugins ./plugins
COPY --from=deps /app/babel.config.js ./
COPY --from=deps /app/.babelrc* ./

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 gatsby

# Change ownership
RUN chown -R gatsby:nodejs /app

USER gatsby

# Expose the port
EXPOSE 3666

# Set environment variables
ENV NODE_ENV=development
ENV PORT=3666
ENV HOST=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3666/ || exit 1

# Start Gatsby development server
CMD ["npx", "gatsby", "develop", "--host", "0.0.0.0", "--port", "3666", "--verbose"]