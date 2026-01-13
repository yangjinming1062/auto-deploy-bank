# Dockerfile - Spring Cloud API Gateway
# Delegates to fangjia-fsh-api service directory
FROM alpine:latest AS delegate

# Copy the actual Dockerfile and build context from service directory
COPY Spring-Cloud-Book-Code-1/fangjia-fsh-api/Dockerfile /tmp/Dockerfile.service
COPY Spring-Cloud-Book-Code-1/fangjia-fsh-api/ /tmp/service-build-context/

# Use the service-specific Dockerfile for multi-stage build
# Note: Actual build happens in fangjia-fsh-api directory with docker-compose
