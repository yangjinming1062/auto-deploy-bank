# Build stage
FROM node:20-alpine AS builder

WORKDIR /home/ubuntu/deploy-projects/33f55019a94710f401e17074

# Install pnpm
RUN npm install -g pnpm

# Copy entire project
COPY . .

# Install dependencies
RUN pnpm install

# Build all packages
RUN pnpm nx run-many -t build

# Production stage
FROM node:20-alpine AS production

WORKDIR /home/ubuntu/deploy-projects/33f55019a94710f401e17074

# Copy built packages from builder
COPY --from=builder /home/ubuntu/deploy-projects/33f55019a94710f401e17074/node_modules ./node_modules
COPY --from=builder /home/ubuntu/deploy-projects/33f55019a94710f401e17074/packages ./packages
COPY --from=builder /home/ubuntu/deploy-projects/33f55019a94710f401e17074/server.ts .

# Install tsx for running TypeScript
RUN npm install -g tsx

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Run the server
CMD ["npx", "tsx", "server.ts"]