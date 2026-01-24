FROM node:20-slim

# Install dependencies for TensorFlow.js native bindings
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    libc6 \
    libc6-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/adc15635ba086798b0f17751

# Enable corepack for pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files for dependency caching
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Copy all workspace directories for dependency resolution
COPY examples examples/
COPY models models/
COPY packages packages/

# Install root dependencies
RUN pnpm install --frozen-lockfile

# Copy package.json for nodejs example separately and install with npm
COPY examples/nodejs/package.json examples/nodejs/package.json
RUN cd examples/nodejs && npm install --no-audit --no-fund

# Copy the rest of the application
COPY . .

# Build the core package
RUN pnpm --filter upscaler run build

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8080

# Expose the internal port
EXPOSE 8080

# Run the Node.js example server
CMD ["node", "examples/nodejs/src/index.js", "0.0.0.0", "8080"]