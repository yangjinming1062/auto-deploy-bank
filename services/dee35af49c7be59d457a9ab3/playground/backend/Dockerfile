# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Multi-stage build for Apache Beam Playground Backend (Go)
ARG GO_VERSION=1.20
FROM golang:${GO_VERSION}-bullseye AS builder

# Setup Go Environment
ENV GOPATH=/go
ENV PATH=$GOPATH/bin:$PATH
WORKDIR /go/src/playground/backend

# Copy go mod files and source code together for proper module resolution
COPY playground/backend/go.mod playground/backend/go.sum ./
COPY playground/backend/cmd ./cmd
COPY playground/backend/internal ./internal
COPY playground/backend/configs ./configs

# Download dependencies and build
RUN go mod download && \
    go mod tidy -v && \
    cd cmd/server && \
    go build -ldflags="-X main.BuildCommitHash=${GIT_COMMIT:-<unknown>} -X main.BuildCommitTimestamp=${GIT_TIMESTAMP:-0}" -o /go/bin/server_go_backend

# Runtime stage
FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV SERVER_IP=0.0.0.0
ENV SERVER_PORT=8080
ENV APP_WORK_DIR=/opt/playground/backend/
ENV BEAM_SDK=SDK_UNSPECIFIED
ENV SDK_CONFIG=/opt/playground/backend/sdks.yaml
ENV PROPERTY_PATH=/opt/playground/backend/
ENV PROTOCOL_TYPE=HTTP
ENV CACHE_TYPE=local
ENV CACHE_ADDRESS=localhost:6379
ENV KEY_EXPIRATION_TIME=15m
ENV PIPELINE_EXPIRATION_TIMEOUT=10m
ENV LAUNCH_SITE=local
ENV NUM_PARALLEL_JOBS=20

# Install minimal runtime dependencies
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    sed -ri 's|http://deb\.debian\.org|https://deb.debian.org|g' /etc/apt/sources.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends; \
    rm -rf /var/lib/apt/lists/*

# Copy built binary
COPY --from=builder /go/bin/server_go_backend /opt/playground/backend/

# Copy required configuration files
COPY playground/backend/properties.yaml /opt/playground/backend/properties.yaml
COPY playground/sdks.yaml /opt/playground/backend/sdks.yaml
COPY playground/sdks-emulator.yaml /opt/playground/backend/sdks-emulator.yaml
COPY playground/backend/configs /opt/playground/backend/configs/

# Create working directory
WORKDIR /opt/playground/backend

# Expose the server port
EXPOSE 8080

# Run the server
CMD ["/opt/playground/backend/server_go_backend"]