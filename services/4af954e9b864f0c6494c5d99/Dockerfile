# syntax=docker/dockerfile:1

# Stage 1: Frontend builder
FROM node:24.13.0-alpine@sha256:931d7d57f8c1fd0e2179dbff7cc7da4c9dd100998bc2b32afc85142d8efbc213 AS frontendbuilder

WORKDIR /build

ENV PNPM_CACHE_FOLDER=.cache/pnpm/
ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV CYPRESS_INSTALL_BINARY=0

COPY frontend/pnpm-lock.yaml frontend/package.json frontend/.npmrc ./
COPY frontend/patches ./patches
RUN npm install -g corepack && corepack enable && \
    pnpm install --frozen-lockfile
COPY frontend/ ./
ARG RELEASE_VERSION=dev
RUN echo "{\"VERSION\": \"${RELEASE_VERSION/-g/-}\"}" > src/version.json && pnpm run build

# Stage 2: API Builder
FROM golang:1.25-alpine AS apibuilder

WORKDIR /build

# Install build tools and C compiler for CGO
RUN apk add --no-cache gcc musl-dev libc-dev

# Install mage for building
RUN go install github.com/magefile/mage@latest

# Copy go module files first for better caching
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Copy built frontend
COPY --from=frontendbuilder /build/dist ./frontend/dist

# Build the application
ARG RELEASE_VERSION=dev
ENV RELEASE_VERSION=$RELEASE_VERSION

RUN set -ex && \
    export PATH=$PATH:$GOPATH/bin && \
    CGO_ENABLED=1 go build -v -ldflags "-s -w -X code.vikunja.io/api/pkg/version.Version=${RELEASE_VERSION}" -o vikunja

# Stage 3: Runtime image
FROM alpine:3.19 AS runtime

# Install CA certificates, timezone data, and zip for JAR creation
RUN apk add --no-cache ca-certificates tzdata zip

WORKDIR /app/vikunja

# Create non-root user for security
RUN addgroup -g 1000 vikunja && \
    adduser -u 1000 -G vikunja -s /bin/sh -D vikunja

# Copy the built binary and frontend assets
COPY --from=apibuilder /build/vikunja ./vikunja
COPY --from=apibuilder /build/frontend/dist ./frontend/dist

# Create JAR file for security scanner (Go binary packaged as ZIP/JAR for security scanning)
RUN zip -q -r target.jar vikunja && rm vikunja

# Copy config
COPY --from=apibuilder /build/config.json .

# Make target.jar readable
RUN chmod 664 ./target.jar

# Create directories for persistence and scanning
RUN mkdir -p ./files ./db /scan && chown -R vikunja:vikunja . && chown -R vikunja:vikunja /scan

# Copy startup script
COPY --chmod=755 start.sh /start.sh

# Switch to non-root user
USER vikunja

# Expose service port
EXPOSE 3456

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --spider -q http://localhost:3456/api/v1/info || exit 1

# Entry point
ENTRYPOINT ["/start.sh"]