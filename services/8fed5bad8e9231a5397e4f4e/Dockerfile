FROM node:22-alpine AS builder

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/8fed5bad8e9231a5397e4f4e

# Copy only package files first
COPY package.json package-lock.json lerna.json ./
COPY babel.config.js rollup.config.js tsconfig.json eslint.config.js ./
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY packages/ ./packages/

# Install dependencies
ENV DISABLE_POSTINSTALL_SCRIPT=true
RUN npm install --ignore-scripts

# Build the project
RUN npm run build

# Production stage
FROM node:22-alpine

WORKDIR /home/ubuntu/deploy-projects/8fed5bad8e9231a5397e4f4e

# Copy built artifacts from builder
COPY --from=builder /home/ubuntu/deploy-projects/8fed5bad8e9231a5397e4f4e/packages/vega/build ./packages/vega/build
COPY --from=builder /home/ubuntu/deploy-projects/8fed5bad8e9231a5397e4f4e/docs ./docs

# Environment variables
ENV NODE_ENV=production
ENV PORT=8080

# Install serve for hosting static files
RUN npm install -g serve

# Expose the service port
EXPOSE 8080

# Serve the vega package
CMD ["serve", "packages/vega/", "-l", "tcp://0.0.0.0:8080", "-s"]