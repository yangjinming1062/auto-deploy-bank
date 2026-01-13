# Multi-stage build for Apache Curator
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml and download dependencies
COPY pom.xml .
COPY curator-client/pom.xml curator-client/
COPY curator-framework/pom.xml curator-framework/
COPY curator-recipes/pom.xml curator-recipes/
COPY curator-examples/pom.xml curator-examples/
COPY curator-x-async/pom.xml curator-x-async/
COPY curator-x-discovery/pom.xml curator-x-discovery/
COPY curator-x-discovery-server/pom.xml curator-x-discovery-server/
COPY curator-test/pom.xml curator-test/
COPY curator-test-zk35/pom.xml curator-test-zk35/
COPY curator-test-zk36/pom.xml curator-test-zk36/
COPY curator-test-zk37/pom.xml curator-test-zk37/
COPY curator-test-zk38/pom.xml curator-test-zk38/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY curator-client/src curator-client/src
COPY curator-framework/src curator-framework/src
COPY curator-recipes/src curator-recipes/src
COPY curator-examples/src curator-examples/src
COPY curator-x-async/src curator-x-async/src
COPY curator-x-discovery/src curator-x-discovery/src
COPY curator-x-discovery-server/src curator-x-discovery-server/src
COPY curator-test/src curator-test/src
COPY curator-test-zk35/src curator-test-zk35/src
COPY curator-test-zk36/src curator-test-zk36/src
COPY curator-test-zk37/src curator-test-zk37/src
COPY curator-test-zk38/src curator-test-zk38/src

# Build the project and create fat JAR with dependencies
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built fat JAR from builder stage
COPY --from=builder /build/curator-examples/target/curator-examples-*-jar-with-dependencies.jar app.jar

# Create target.jar for security scanning volume mount
RUN cp app.jar target.jar

# Expose service port
EXPOSE 40427

# Run the application
CMD ["java", "-jar", "app.jar"]