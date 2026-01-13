FROM node:20-alpine AS builder

# Install git for npm to fetch dependencies
RUN apk add --no-cache git

# Install dependencies
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy source files
COPY . ./

# Build the plugin
RUN npm run build

# Production stage with http-server
FROM node:20-alpine

# Install git for npm to fetch dependencies
RUN apk add --no-cache git

# Install http-server for serving static files
RUN npm install -g http-server

WORKDIR /app

# Copy built files from builder stage
COPY --from=builder /app/main.js ./
COPY --from=builder /app/styles.css ./
COPY --from=builder /app/manifest.json ./
COPY --from=builder /app/index.html ./

# Expose port 40978
EXPOSE 40978

# Start http-server
ENV PORT=40978
CMD ["http-server", "-p", "40978", "-c-1", "--cors", "--host", "0.0.0.0"]