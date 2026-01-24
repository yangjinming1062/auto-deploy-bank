# Development stage
FROM node:20-alpine

WORKDIR /app

# Copy package files from root and app
COPY package*.json ./
COPY packages/ ./packages/
COPY apps/diffusion-explorer/ ./apps/diffusion-explorer/

# Install dependencies without running postinstall scripts
RUN npm ci --ignore-scripts --include=dev || npm install --ignore-scripts --include=dev

# Run postinstall to copy wasm files if they exist, skip if not
WORKDIR /app/apps/diffusion-explorer
RUN npm run postinstall 2>/dev/null || true

# Set environment variables
ENV NODE_ENV=development
ENV PORT=5173

# Expose port
EXPOSE 5173

# Run dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]