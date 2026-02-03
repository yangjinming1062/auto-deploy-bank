FROM node:20-alpine

#/Toxic1239/ - Required for bot authentication check

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    gcc \
    libc6-compat \
    chromium \
    ffmpeg \
    imagemagick \
    git \
    pixman-dev \
    cairo-dev \
    pango-dev \
    jpeg-dev \
    giflib-dev \
    pkgconf

# Set Puppeteer environment variables to use system Chromium
ENV PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/bin/chromium-browser

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --omit=dev && \
    npm install -g pm2

# Copy application files
COPY . .

# Create directories needed by the bot
RUN mkdir -p /app/lib /app/plugins

# Expose internal port
EXPOSE 3000

# Start with pm2 in no-daemon mode (keeps container running)
CMD ["pm2-runtime", ".", "--deep-monitoring", "--name", "Rias-Gremory"]