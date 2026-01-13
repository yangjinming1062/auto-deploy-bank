FROM node:20-alpine

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy pnpm lockfile and workspace configuration
COPY pnpm-lock.yaml pnpm-workspace.yaml ./
COPY package.json ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy entire project
COPY . .

# Install dependencies for the basic-host-remote example workspaces
RUN cd basic-host-remote && pnpm install

# Build the basic-host-remote example
RUN pnpm --filter basic-host-remote run build

# Expose the host app port
EXPOSE 3001

# Start both apps (host and remote)
# App1 (host) on 3001, App2 (remote) on 3002
CMD ["sh", "-c", "cd /app/basic-host-remote/app1 && PORT=3001 npm run serve > /tmp/app1.log 2>&1 & sleep 2 && cd /app/basic-host-remote/app2 && PORT=3002 npm run serve > /tmp/app2.log 2>&1 & wait"]