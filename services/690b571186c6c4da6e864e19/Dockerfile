# Root-level Dockerfile that builds the www service
# This delegates to www/Dockerfile for the actual build process

FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json pnpm-lock.yaml* ./

RUN corepack enable pnpm && \
    pnpm install --no-frozen-lockfile

COPY . .

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV DISABLE_REWRITES=true

# Install www dependencies and build
COPY www/package.json www/pnpm-lock.yaml* ./www/
RUN corepack enable pnpm && \
    cd www && \
    pnpm install --no-frozen-lockfile

# Build the application (run from www directory)
RUN corepack enable pnpm && \
    cd www && \
    pnpm run build:blogSearchDev && \
    pnpm run build:templates && \
    pnpm run build:next

# Stage 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app/www

ENV NODE_ENV=production
ENV PORT=3000
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy package files and install production deps
COPY www/package.json ./
RUN corepack enable pnpm && \
    pnpm install --prod --no-frozen-lockfile

# Copy built artifacts
COPY --from=builder /app/www/public ./public
COPY --from=builder /app/www/.next ./.next

# Set ownership for Next.js files
RUN chown -R nextjs:nodejs /app/www

USER nextjs

EXPOSE 3000

CMD ["npm", "start"]