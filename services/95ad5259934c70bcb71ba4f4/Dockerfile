# Development stage for SvelteKit app (npm workspaces monorepo)
FROM node:20-alpine

WORKDIR /app

# Copy full monorepo structure first (needed for npm to detect workspaces)
COPY diffusion-explorer/ ./diffusion-explorer/

# Install dependencies - npm will detect and install all workspaces
# Use --ignore-scripts to skip postinstall during workspace installation
WORKDIR /app/diffusion-explorer
RUN npm install --ignore-scripts --include=dev

# Run postinstall in the app to copy wasm files after deps are installed
WORKDIR /app/diffusion-explorer/apps/diffusion-explorer
RUN npm run postinstall 2>/dev/null || true

# Set environment variables
ENV NODE_ENV=development
ENV PORT=5173

# Expose port
EXPOSE 5173

# Run dev server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]