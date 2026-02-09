FROM node:16-alpine

# Install build dependencies for canvas (native compilation)
RUN apk add --no-cache python3 make g++ libc-dev pkgconfig pixman-dev libpng-dev jpeg-dev cairo-dev pango-dev libjpeg-turbo-dev

WORKDIR /home/ubuntu/deploy-projects/0229521e86f5fa498425bf8d

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies (legacy-peer-deps needed for older eslint conflict)
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build the project (runs tests, cleans dist, generates version, builds dev and prod)
RUN npm run build

# Set environment variables
ENV NODE_ENV=production
ENV PORT=41517

# Expose the port
EXPOSE 41517

# Run a simple server to serve the built dist files
CMD ["npx", "serve", "-l", "41517", "dist"]