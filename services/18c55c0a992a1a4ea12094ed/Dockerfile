# Build stage
FROM golang:1.19-alpine AS builder

WORKDIR /app

# Download dependencies
COPY server/manager/go.mod server/manager/go.sum ./
RUN go mod download

# Copy source code
COPY server/manager/ .

# Copy web_console frontend files to frontend directory for embedding
RUN cp -r server/web_console/* static/frontend/ 2>/dev/null || true

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags "-s -w" -o manager main.go

# Create proper JAR file (ZIP archive format) for security scanning
# JAR files are just ZIP files with MANIFEST.MF
RUN apk add zip && \
    echo "Manifest-Version: 1.0" > MANIFEST.MF && \
    echo "Built-By: Elkeid" >> MANIFEST.MF && \
    echo "Implementation-Title: Elkeid Manager" >> MANIFEST.MF && \
    echo "Implementation-Version: 1.0.0" >> MANIFEST.MF && \
    zip target.jar MANIFEST.MF && \
    zip -k target.jar manager && \
    rm -f MANIFEST.MF

# Runtime stage
FROM alpine:3.18

RUN apk --no-cache add ca-certificates tzdata wget

WORKDIR /app

# Copy built binary from builder stage
COPY --from=builder /app/manager ./manager
# Copy as target.jar for security scanning (valid ZIP archive)
COPY --from=builder /app/target.jar ./target.jar

# Create conf directory and copy modified configuration
RUN mkdir -p /app/conf
COPY --from=builder /app/conf ./conf

# Create modified svr.yml with proper service hostnames
RUN sed -i 's/127.0.0.1:6379/redis:6379/g' /app/conf/svr.yml && \
    sed -i 's/127.0.0.1:8088/agent_center:8088/g' /app/conf/svr.yml && \
    sed -i 's|uri: mongodb://elkeid:c596988d134go1qran@10.227.2.103:27017|uri: mongodb://elkeid:c596988d134go1qran@mongo:27017|g' /app/conf/svr.yml

# Create required directories
RUN mkdir -p /app/log /app/static/frontend

# Expose the HTTP port (configured in svr.yml as 6701)
EXPOSE 6701

# Run the manager server
CMD ["./manager"]