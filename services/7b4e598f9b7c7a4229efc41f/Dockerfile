FROM node:20-alpine

# Install wget for healthcheck
RUN apk add --no-cache wget

# Install verdaccio and verdaccio-audit
RUN npm install -g verdaccio verdaccio-audit

# Create necessary directories
RUN mkdir -p /verdaccio/storage /verdaccio/cache

# Copy configuration
COPY verdaccio.yaml /verdaccio/config.yaml

# Expose Verdaccio default port
EXPOSE 4873

# Set working directory
WORKDIR /verdaccio

# Run verdaccio
CMD ["verdaccio", "--config", "/verdaccio/config.yaml", "--listen", "http://0.0.0.0:4873"]