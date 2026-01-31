FROM node:22-alpine

# Install pnpm
ENV PNPM_HOME=/pnpm
ENV PATH=$PNPM_HOME/bin:$PATH

RUN corepack enable && corepack prepare pnpm@10.28.0 --activate

WORKDIR /app

# Copy package files and patches
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml patches/ ./

# Copy source code
COPY . .

# Install all dependencies (including workspace packages)
RUN pnpm install

# Build all packages
RUN pnpm build

# Build the website
RUN cd website && pnpm install && pnpm build

# Expose the preview server port (rspress preview default)
EXPOSE 4173

# Set environment variables
ENV NODE_ENV=production
ENV PORT=4173
ENV HOST=0.0.0.0

# Start the documentation preview server
CMD ["sh", "-c", "cd website && pnpm exec rspress preview --host 0.0.0.0"]