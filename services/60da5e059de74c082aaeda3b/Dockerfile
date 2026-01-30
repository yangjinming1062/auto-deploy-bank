FROM node:20-alpine

WORKDIR /app

# Copy package files first
COPY package.json yarn.lock ./
COPY packages packages/

# Install dependencies including workspace packages
RUN yarn install --frozen-lockfile --non-interactive

# Copy the rest of the source files
COPY fixtures fixtures/
COPY scripts scripts/
COPY .yarnrc .npmrc biome.json ./

# Expose port (Vite dev server default)
EXPOSE 53005

# Start Vite dev server for xgplayer fixture
CMD ["node", "./scripts/cli.js", "dev", "fixtures/xgplayer", "-p", "53005"]