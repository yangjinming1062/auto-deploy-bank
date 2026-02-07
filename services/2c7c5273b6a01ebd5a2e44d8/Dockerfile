FROM node:20-alpine

# Install build dependencies for native modules (canvas, etc.)
RUN apk add --no-cache \
    make \
    g++ \
    python3 \
    curl \
    bash \
    pkgconfig \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    libffi-dev \
    musl-dev \
    busybox

WORKDIR /home/ubuntu/deploy-projects/2c7c5273b6a01ebd5a2e44d8

# Copy package files and Makefile first for install script
COPY package*.json Makefile ./

# Copy source code needed for install
COPY src ./src
COPY lib ./lib

# Install production dependencies (skipping install script)
RUN npm ci --only=production --ignore-scripts

# Copy remaining source code
COPY . .

# Build phaseA (Pyret compiler/interpreter)
RUN make phaseA

# Set permissions for scripts
RUN chmod +x src/scripts/phase0 src/scripts/phaseA src/scripts/run-phase

# Environment variables
ENV NODE_ENV=production
ENV PORT=8888
ENV PHASE=phaseA

# Expose the service port
EXPOSE 8888

# Default command - shows usage info
CMD ["node", "build/phaseA/pyret.jarr", "--help"]