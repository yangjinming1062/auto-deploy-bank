FROM node:20-alpine

# Install git for GitHub dependencies
RUN apk add --no-cache git

# Install pnpm
ENV PNPM_VERSION=8.15.9
RUN npm install -g pnpm@${PNPM_VERSION}

WORKDIR /home/ubuntu/deploy-projects/0fdc5ce98767679827d7a5fc

# Copy package files
COPY package*.json ./
COPY pnpm-lock.yaml ./
COPY pnpm-workspace.yaml ./

# Copy source code
COPY . .

# Install dependencies after source code is copied to ensure all workspace deps are linked
RUN pnpm install --no-frozen-lockfile

# Build core packages first (required for dev/app-main)
WORKDIR /home/ubuntu/deploy-projects/0fdc5ce98767679827d7a5fc
RUN pnpm build

# Build dev/app-main (webpack will bundle all dependencies)
WORKDIR /home/ubuntu/deploy-projects/0fdc5ce98767679827d7a5fc/dev/app-main
RUN pnpm build

# Install http-server for serving production build
RUN npm install -g http-server

# Expose the app port
EXPOSE 8090

# Set production environment
ENV NODE_ENV=production
ENV PORT=8090

# Change back to app directory and serve static files
WORKDIR /home/ubuntu/deploy-projects/0fdc5ce98767679827d7a5fc/dev/app-main

CMD ["sh", "-c", "http-server dist -p $PORT -c-1 --host 0.0.0.0"]