# Multi-stage build for LibRec recommender system library

# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml first for better Docker layer caching
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the project
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM ubuntu:22.04

# Install Java 17
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

# Install bash
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy JAR from builder stage (copy to /app/target.jar for volume mount security scanning)
COPY --from=builder /app/target/librec-1.4.jar app/target.jar

# Copy demo configurations and datasets
COPY demo ./demo

# Create Results directory
RUN mkdir -p Results

# Set default command to run LibRec web service
CMD ["java", "-cp", "app/target.jar", "librec.main.LibRecWebService"]