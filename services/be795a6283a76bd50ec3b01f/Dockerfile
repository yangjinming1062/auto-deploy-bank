FROM node:20-alpine

# Install pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@8.15.0 --activate

WORKDIR /app

# Copy Rush configuration first
COPY rush.json ./
COPY common/config/rush/pnpm-config.json ./common/config/rush/pnpm-config.json
COPY common/config/rush/.npmrc ./common/config/rush/.npmrc
COPY common/config/rush/.pnpmfile.cjs ./common/config/rush/.pnpmfile.cjs

# Copy source directories
COPY packages packages/
COPY docs docs/
COPY share share/
COPY tools tools/

# Create pnpm-workspace.yaml for pnpm to understand the monorepo structure
RUN cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'packages/*'
  - 'docs'
  - 'share/*'
  - 'tools/*'
EOF

# Install dependencies
RUN pnpm install --no-frozen-lockfile

# Build all packages (recursive across workspace)
RUN pnpm -r run build

# Build docs
WORKDIR /app/docs
RUN npm run build

# Expose the port (3020 from vite.config.js)
EXPOSE 3020

# Serve the built files (--no-open prevents browser auto-open)
CMD ["npx", "vite", "preview", "--host", "--port", "3020", "--no-open"]