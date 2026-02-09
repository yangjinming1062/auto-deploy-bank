FROM node:22-alpine

# Install pnpm globally
RUN npm install -g pnpm@9

WORKDIR /home/ubuntu/deploy-projects/7b4e598f9b7c7a4229efc41f

# Copy entire project first (required for workspace dependencies)
COPY . .

# Install dependencies (includes all workspace packages)
RUN pnpm install

# Expose verdaccio port (default)
EXPOSE 4873

# Run verdaccio (local npm registry)
CMD ["npx", "verdaccio", "--config", "verdaccio.yaml"]