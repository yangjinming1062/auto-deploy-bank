# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 as builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build fatjar with dependencies (skip tests for faster build)
RUN mvn clean package -DskipTests -B -Dgpg.skip=true

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /home/ubuntu/deploy-projects/a93556c2b37df50b72f4db50

# Create cache directory for Pyserini indexes (from context)
ENV ANSERINI_INDEX_CACHE=/home/ubuntu/deploy-projects/a93556c2b37df50b72f4db50/.cache/pyserini/indexes

# Copy the fatjar from builder stage
# The shade plugin creates: anserini-1.5.1-SNAPSHOT-fatjar.jar
# Copy to both /home/ubuntu/deploy-projects/a93556c2b37df50b72f4db50.jar (for volume mount) and app.jar (for running)
COPY --from=builder /app/target/anserini-*-fatjar.jar /home/ubuntu/deploy-projects/a93556c2b37df50b72f4db50.jar
COPY --from=builder /app/target/anserini-*-fatjar.jar app.jar

# Create directories for cache
RUN mkdir -p ${ANSERINI_INDEX_CACHE}

# Create wrapper script to keep container running
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'echo "Anserini CLI ready - use: docker exec <container> java -cp app.jar <class> <args>"' >> /entrypoint.sh && \
    echo 'while true; do sleep 3600; done' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Default command - keep container alive with infinite loop
CMD ["/entrypoint.sh"]