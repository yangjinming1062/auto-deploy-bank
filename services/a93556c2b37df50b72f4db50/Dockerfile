# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the project (skip tests, build fatjar)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Install Python3 and wget for HTTP server and healthcheck
RUN apk add --no-cache python3 wget

# Copy the fatjar from builder as target.jar for security scanning
# The shade plugin creates *-fatjar.jar which we rename to target.jar
COPY --from=builder /app/target/*-fatjar.jar target.jar

# Copy startup script and server
COPY start.sh /app/start.sh
COPY server.py /app/server.py
RUN chmod +x /app/start.sh /app/server.py

# Set environment variable for index cache
ENV ANSERINI_INDEX_CACHE=/root/.cache/pyserini/indexes

# Run startup script which handles both daemon mode and command execution
CMD ["/app/start.sh"]