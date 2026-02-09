# Build stage and production in one
FROM node:20-alpine

# Install pnpm
RUN npm install -g pnpm@9.10.0

# Create app directory
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY patches ./patches

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Install dependencies for all workspace packages
RUN pnpm install --recursive

# Build core packages first (in dependency order)
RUN cd packages/react-router && pnpm run build
RUN cd packages/react-router-dom && pnpm run build
RUN cd packages/react-router-node && pnpm run build
RUN cd packages/react-router-express && pnpm run build
RUN cd packages/react-router-architect && pnpm run build
RUN cd packages/react-router-cloudflare && pnpm run build
RUN cd packages/react-router-dev && pnpm run build
RUN cd packages/react-router-fs-routes && pnpm run build
RUN cd packages/react-router-remix-routes-option-adapter && pnpm run build
RUN cd packages/create-react-router && pnpm run build
RUN cd packages/react-router-serve && pnpm run build

# Build the framework playground app
WORKDIR /app/playground/framework
RUN pnpm install && pnpm build

# Environment variables
ENV NODE_ENV=development
ENV USE_SOURCE=true
ENV PORT=3000

# Expose port
EXPOSE 3000

# Start command
CMD ["pnpm", "start"]