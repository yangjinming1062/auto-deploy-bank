# Dockerfile for LibRec - multi-stage build with web interface

# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml first for better Docker layer caching
COPY librec/pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY librec/src ./src

# Build the project (shade plugin creates uber jar with LibRec as main class)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image with Python for web server
FROM eclipse-temurin:17-jre-alpine AS runtime

# Install Python and pip for web server
RUN apk add --no-cache python3 py3-pip bash

# Set working directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/librec-*.jar /app/target.jar

# Copy demo configurations and datasets
COPY librec/demo ./demo

# Copy web server
COPY web/ ./web

# Install Python dependencies (use --break-system-packages for Alpine)
RUN pip3 install --no-cache-dir --break-system-packages -r web/requirements.txt

# Create Results directory
RUN mkdir -p Results

# Create results symlink for web access
RUN ln -s /app/Results /app/demo/Results || true

# Run web server as main process
EXPOSE 5000

CMD ["sh", "-c", "python3 /app/web/server.py"]