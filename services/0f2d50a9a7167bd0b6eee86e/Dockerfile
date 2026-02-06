##
## Build Lowcoder api-service application (selfhost profile)
##
FROM maven:3.9-eclipse-temurin-17 AS builder

# Build lowcoder-api-service with selfhost profile
COPY ./server/api-service /app
WORKDIR /app

# Download dependencies and build the application
RUN mvn -f pom.xml clean package -DskipTests -Pselfhost -B

# Create required folder structure
RUN mkdir -p /lowcoder/api-service/config /lowcoder/api-service/logs /lowcoder/plugins

# Copy lowcoder server configuration
COPY server/api-service/lowcoder-server/src/main/resources/application.yaml /lowcoder/api-service/config/

# Add bootstrap scripts
COPY deploy/docker/api-service/entrypoint.sh /lowcoder/api-service/entrypoint.sh
COPY deploy/docker/api-service/init.sh /lowcoder/api-service/init.sh

ENV JAVA_OPTS="-Xmx2G -Xms512M"
RUN chmod +x /lowcoder/api-service/*.sh

##
## Runtime image for Lowcoder api-service
##
FROM eclipse-temurin:17-jdk-alpine AS runtime

RUN addgroup -S -g 9001 lowcoder \
    && adduser -S -u 9001 -G lowcoder -s /bin/false -D -H lowcoder

# Install gosu for privilege escalation
RUN apk add --no-cache gosu

# Copy from builder
COPY --chown=lowcoder:lowcoder --from=builder /lowcoder/api-service /lowcoder/api-service

# Copy the built JAR file (extract from assembly directory)
COPY --chown=lowcoder:lowcoder --from=builder /app/lowcoder-server/target/lowcoder-api-service-bin/lowcoder-api-service.jar /lowcoder/api-service/lowcoder-api-service.jar
COPY --chown=lowcoder:lowcoder --from=builder /app/lowcoder-server/target/lowcoder-api-service-bin/libs /lowcoder/api-service/libs
COPY --chown=lowcoder:lowcoder --from=builder /app/lowcoder-server/target/lowcoder-api-service-bin/plugins /lowcoder/api-service/plugins

# Create logs directory symlink for null device
RUN ln -s /dev/null /lowcoder/api-service/logs/main.log \
    && ln -s /dev/null /lowcoder/api-service/logs/query-error.log \
    && chmod 777 /lowcoder/api-service/logs/main.log \
    && chmod 777 /lowcoder/api-service/logs/query-error.log

# Set working directory
WORKDIR /lowcoder/api-service

# Expose the API service port
EXPOSE 8080

# Run the application using the entrypoint script
CMD ["/bin/sh", "/lowcoder/api-service/entrypoint.sh"]