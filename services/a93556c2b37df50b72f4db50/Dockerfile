# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Expose default port
EXPOSE 8080

# Set default port environment variable
ENV PORT=8080

# Copy the fatjar from builder stage
# The shade plugin creates: anserini-{version}-fatjar.jar
# Renamed to target.jar for security scanner compatibility
COPY --from=builder /app/target/anserini-*-fatjar.jar target.jar

# Create entrypoint script that maps command names to main classes
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'PORT=${PORT:-8080}' >> /entrypoint.sh && \
    echo 'if [ "$1" = "server" ]; then' >> /entrypoint.sh && \
    echo '  exec java -cp /app/target.jar io.anserini.server.HealthServer' >> /entrypoint.sh && \
    echo 'elif [ -z "$1" ]; then' >> /entrypoint.sh && \
    echo '  exec java -cp /app/target.jar io.anserini.server.HealthServer' >> /entrypoint.sh && \
    echo 'else' >> /entrypoint.sh && \
    echo '  MAIN_CLASS=""' >> /entrypoint.sh && \
    echo '  case "$1" in' >> /entrypoint.sh && \
    echo '    IndexCollection) MAIN_CLASS="io.anserini.index.IndexCollection" ; shift ;;' >> /entrypoint.sh && \
    echo '    IndexHnswDenseVectors) MAIN_CLASS="io.anserini.index.IndexHnswDenseVectors" ; shift ;;' >> /entrypoint.sh && \
    echo '    IndexInvertedDenseVectors) MAIN_CLASS="io.anserini.index.IndexInvertedDenseVectors" ; shift ;;' >> /entrypoint.sh && \
    echo '    IndexFlatDenseVectors) MAIN_CLASS="io.anserini.index.IndexFlatDenseVectors" ; shift ;;' >> /entrypoint.sh && \
    echo '    SearchCollection) MAIN_CLASS="io.anserini.search.SearchCollection" ; shift ;;' >> /entrypoint.sh && \
    echo '    SearchHnswDenseVectors) MAIN_CLASS="io.anserini.search.SearchHnswDenseVectors" ; shift ;;' >> /entrypoint.sh && \
    echo '    SearchFlatDenseVectors) MAIN_CLASS="io.anserini.search.SearchFlatDenseVectors" ; shift ;;' >> /entrypoint.sh && \
    echo '    FuseRuns) MAIN_CLASS="io.anserini.fusion.FuseRuns" ; shift ;;' >> /entrypoint.sh && \
    echo '    RunMsMarco) MAIN_CLASS="io.anserini.reproduce.RunMsMarco" ; shift ;;' >> /entrypoint.sh && \
    echo '    RunBeir) MAIN_CLASS="io.anserini.reproduce.RunBeir" ; shift ;;' >> /entrypoint.sh && \
    echo '    RunBright) MAIN_CLASS="io.anserini.reproduce.RunBright" ; shift ;;' >> /entrypoint.sh && \
    echo '    *) echo "Unknown command: $1"; echo "Available commands: IndexCollection, IndexHnswDenseVectors, IndexInvertedDenseVectors, IndexFlatDenseVectors, SearchCollection, SearchHnswDenseVectors, SearchFlatDenseVectors, FuseRuns, RunMsMarco, RunBeir, RunBright, server"; exit 1 ;;' >> /entrypoint.sh && \
    echo '  esac' >> /entrypoint.sh && \
    echo '  exec java -cp /app/target.jar "$MAIN_CLASS" "$@"' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]