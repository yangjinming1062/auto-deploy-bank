# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-8 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .

# Copy source code
COPY src ./src

# Install the local JAR dependency from libs/
COPY libs/algorithmfoundry-shade-culled-1.3.jar /tmp/algorithmfoundry-shade-culled-1.3.jar
RUN mvn install:install-file -DgroupId=algorithmfoundry -DartifactId=algorithmfoundry-shade-culled \
    -Dversion=1.3 -Dpackaging=jar -Dfile=/tmp/algorithmfoundry-shade-culled-1.3.jar -B

# Build the JAR (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

# Set working directory
WORKDIR /app

# Install required utilities for healthcheck
RUN apk add --no-cache curl

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app
USER app

# Copy the built JAR from builder stage and rename to target.jar for security scanning
COPY --from=builder /app/target/htm.java-*.jar /app/target.jar

# Set the entry point to run the Java application with JAVA_OPTS
CMD ["sh", "-c", "java $JAVA_OPTS -jar /app/target.jar"]