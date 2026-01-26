# AWS Landing Zone Accelerator on AWS - Docker Image
# This image is used for CDK deployment operations

FROM node:20-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/436d591082a470dc77c1b742

# Set Node.js options for memory management
ENV NODE_OPTIONS="--max_old_space_size=12288 --no-warnings"
ENV CDK_NEW_BOOTSTRAP=1
ENV NODE_ENV=production
ENV HUSKY=0
ENV YARN_ENABLE_IMMUTABLE_CACHE=false
ENV NPM_CONFIG_AUDIT=false
ENV NPM_CONFIG_FUND=false

# Copy all source files
COPY source/package*.json source/yarn.lock source/lerna.json ./
COPY source/packages ./packages
COPY source/. .

# Install dependencies - first try without ignore-scripts (installs all deps despite husky error)
RUN yarn install --frozen-lockfile --network-timeout 300000 || true

# Install missing dependencies that aren't properly linked with --ignore-scripts
RUN yarn add mri@1.2.0 glob@13.0.0 --ignore-workspace-root-check --ignore-scripts || true

# Default command - keep container running for exec access
CMD ["sleep", "infinity"]