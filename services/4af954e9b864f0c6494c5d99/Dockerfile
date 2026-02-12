# syntax=docker/dockerfile:1@sha256:b6afd42430b15f2d2a4c5a02b919e98a525b785b1aaff16747d2f623364e39b6
FROM --platform=$BUILDPLATFORM node:24.13.0-alpine@sha256:931d7d57f8c1fd0e2179dbff7cc7da4c9dd100998bc2b32afc85142d8efbc213 AS frontendbuilder

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

FROM --platform=$BUILDPLATFORM ghcr.io/techknowlogick/xgo:go-1.25.x@sha256:11ac5e6cb8767caea0c62c420e053cb69554638ec255f9bbef8ed411e70c9eec AS apibuilder

RUN go install github.com/magefile/mage@latest && \
    mv /go/bin/mage /usr/local/go/bin

WORKDIR /go/src/code.vikunja.io/api
COPY . ./
COPY --from=frontendbuilder /build/dist ./frontend/dist

ARG TARGETOS TARGETARCH TARGETVARIANT RELEASE_VERSION=dev
ENV RELEASE_VERSION=$RELEASE_VERSION

RUN export PATH=$PATH:$GOPATH/bin && \
	RELEASE_VERSION=${RELEASE_VERSION:-dev} mage build:clean && \
    mage release:xgo "${TARGETOS}/${TARGETARCH}/${TARGETVARIANT}"

#  ┬─┐┬ ┐┌┐┐┌┐┐┬─┐┬─┐
#  │┬┘│ │││││││├─ │┬┘
#  ┘└┘┘─┘┘└┘┘└┘┴─┘┘└┘

# Build stage for security scanner - creates target.jar
FROM golang:1.25-alpine AS scannerbuilder

WORKDIR /src
COPY . .
COPY --from=frontendbuilder /build/dist ./frontend/dist

ARG RELEASE_VERSION=dev
ENV RELEASE_VERSION=$RELEASE_VERSION

RUN apk add --no-cache git zip && \
    # Create empty frontend dist if not exists for build
    mkdir -p frontend/dist && touch frontend/dist/index.html && \
    # Build Go binary directly for linux/amd64
    export CGO_ENABLED=0 && \
    go build -tags osusergo -ldflags "-X code.vikunja.io/api/pkg/version.Version=${RELEASE_VERSION} -X main.Tags=osusergo " -o /tmp/vikunja-binary . && \
    # Create a valid ZIP archive containing the binary (JAR is just ZIP format)
    cd /tmp && zip -r target.jar vikunja-binary && \
    mv /tmp/target.jar /src/target.jar

# The actual image
FROM scratch

LABEL org.opencontainers.image.authors='maintainers@vikunja.io'
LABEL org.opencontainers.image.url='https://vikunja.io'
LABEL org.opencontainers.image.documentation='https://vikunja.io/docs'
LABEL org.opencontainers.image.source='https://code.vikunja.io/vikunja'
LABEL org.opencontainers.image.licenses='AGPLv3'
LABEL org.opencontainers.image.title='Vikunja'

WORKDIR /app/vikunja
ENTRYPOINT [ "/app/vikunja/vikunja" ]
EXPOSE 3456
USER 1000

ENV VIKUNJA_SERVICE_ROOTPATH=/app/vikunja/
ENV VIKUNJA_DATABASE_PATH=/db/vikunja.db

COPY --from=apibuilder /build/vikunja-* vikunja
COPY --from=apibuilder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
# Copy target.jar for security scanner
COPY --from=scannerbuilder /src/target.jar /app/target.jar
