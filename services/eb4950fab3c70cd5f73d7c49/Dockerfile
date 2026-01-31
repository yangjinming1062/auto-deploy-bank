FROM node:20-alpine

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9.5.0 --activate

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml .npmrc ./

# Copy workspace package files
COPY packages/*/package.json packages/*/package.json

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Install dependencies in workspace packages to create proper symlinks
WORKDIR /app/packages/vite-plugin-arco-vue-docs
RUN pnpm install

WORKDIR /app/packages/arco-vue-scripts
RUN pnpm install

# Build workspace dependencies (order matters: vite-plugin-arco-vue-docs before arco-vue-scripts)
WORKDIR /app/packages/vite-plugin-arco-vue-docs
RUN pnpm run build

WORKDIR /app/packages/arco-vue-scripts
RUN pnpm run build

# Reinstall to create bin symlinks after building
WORKDIR /app
RUN pnpm install

# Generate icons and run init for web-vue
WORKDIR /app/packages/web-vue
RUN pnpm run icongen && pnpm run lessgen

# Build the component library
WORKDIR /app
RUN pnpm build:component

# Install serve for running the built output
RUN npm install -g serve

# Expose the port
EXPOSE 40634

# Keep container running with serve on built files
CMD ["serve", "-s", "packages/web-vue/dist", "-l", "40634"]