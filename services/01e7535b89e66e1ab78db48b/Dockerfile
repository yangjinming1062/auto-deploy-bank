# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project structure
COPY . .

# Build the project (skip tests, enforcer, and checkstyle for faster build)
RUN mvn clean install -DskipTests -Denforcer.skip=true -Dcheckstyle.skip=true -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /opt/opennlp

# Set environment variables for OpenNLP model downloads
ENV OPENNLP_DOWNLOAD_HOME=/root/.opennlp
ENV OPENNLP_DOWNLOAD_BASE_URL=https://dlcdn.apache.org/opennlp/
ENV OPENNLP_DOWNLOAD_MODEL_PATH=models/ud-models-1.3/

# Copy built artifacts from builder (only the binary distribution)
COPY --from=builder /app/opennlp-distr/target/apache-opennlp-*-bin.tar.gz ./
RUN tar -xzf apache-opennlp-*-bin.tar.gz --strip-components=1 && \
    rm -f apache-opennlp-*-bin.tar.gz

# Copy the JAR file for security scanning (extracted from lib directory)
# The main JAR files are in lib/, we'll create a target.jar for scanning
COPY --from=builder /app/opennlp-tools/target/opennlp-tools-*.jar /opt/opennlp/lib/target.jar

# Set working directory
WORKDIR /opt/opennlp

# Expose the service port
EXPOSE 40180

# Run the HTTP server
CMD ["java", "-cp", "/opt/opennlp/lib/*", "opennlp.tools.servers.OpennlpHttpServer"]