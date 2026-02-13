FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/5e5c581c85f4eba6d5688d82

# Install dependencies for browsers
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    udev \
    wget \
    python3 \
    make \
    g++

# Set environment variables for headless browser
ENV PUPPETEER_SKIP_DOWNLOAD=true \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    CHROME_PATH=/usr/bin/chromium-browser \
    CHROMIUM_PATH=/usr/bin/chromium-browser

# Copy package files
COPY package*.json ./

# Copy lock file for dependency installation
COPY package-lock.json ./

# Install all dependencies (needed for build)
RUN npm ci

# Copy source code
COPY . .

# Build the project (using custom script to skip problematic third-party notice generation)
RUN node utils/build/custom_build.js

# Expose the server port
EXPOSE 3000

# Set environment variables for service mode
ENV PWTEST_UNDER_TEST=1 \
    PWTEST_MODE=default \
    PLAYWRIGHT_SERVICE_OS=linux

# Run the Playwright server
CMD ["node", "packages/playwright-core/cli.js", "run-server", "--port", "3000", "--host", "0.0.0.0"]