# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy entire project for multi-module Maven build
COPY . .

# Build the project
RUN mvn clean install -T 1C -Psofaark -P!single-bootstrap -Dmaven.test.skip=true -am -pl boot/all-in-one-bootstrap && \
    cp /app/boot/all-in-one-bootstrap/target/allinone-executable.jar /app/target.jar

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

# Install bash and net-tools for healthcheck
RUN apk add --no-cache bash net-tools

ENV deploy_path=/home/admin/deploy
ENV app_name=lookoutall

# Create non-root user
RUN addgroup -g 1000 app && \
    adduser -u 1000 -G app -s /bin/sh -D app

WORKDIR ${deploy_path}

# Copy the built artifact from builder stage (both app.jar for runtime and target.jar for scanning)
COPY --from=builder /app/target.jar /home/admin/deploy/app.jar
COPY --from=builder /app/target.jar /home/admin/deploy/target.jar

# Copy entrypoint script
COPY docker/entrypoint.sh ${deploy_path}/entrypoint.sh
RUN chmod +x ${deploy_path}/entrypoint.sh

# Create directories for volumes
RUN mkdir -p /home/admin/logs /home/admin/lookout_gateway_queue_cache && \
    chown -R app:app /home/admin

# Expose application ports (gateway:7200, metrics-server:9090, internal:6200)
EXPOSE 7200 9090 6200

# Environment variables for Elasticsearch connection
ENV metrics_exporter_es_host=elasticsearch
ENV metrics_exporter_es_port=9200
ENV spring_data_jest_uri=http://elasticsearch:9200

USER app

ENTRYPOINT ["/home/admin/deploy/entrypoint.sh"]