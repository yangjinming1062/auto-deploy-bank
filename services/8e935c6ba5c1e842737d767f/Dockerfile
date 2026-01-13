# Multi-stage build for LanguageTool Server
# Stage 1: Build stage with Maven and Java 17
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy the entire project (required for Maven multi-module build)
COPY . .

# Patch pom.xml to configure git-commit-id plugin
RUN sed -i 's|<generateGitPropertiesFile>true</generateGitPropertiesFile>|<generateGitPropertiesFile>false</generateGitPropertiesFile>|' pom.xml && \
    sed -i '/<artifactId>git-commit-id-maven-plugin<\/artifactId>/,/<\/configuration>/s|</configuration>|                        <failOnNoGitDirectory>false</failOnNoGitDirectory>\n                        <skip>false</skip>\n                    </configuration>|' pom.xml

# Build only the server module (skip tests for faster build)
# The -am flag builds required dependencies as well
RUN mvn clean package -DskipTests -B -pl languagetool-server -am && \
    cd /app/languagetool-server && \
    mvn dependency:copy-dependencies -DoutputDirectory=target/lib -DincludeScope=runtime

# Stage 2: Runtime stage with minimal JRE
FROM eclipse-temurin:17-jre-alpine

# Set working directory
WORKDIR /app

# Install wget for health check
RUN apk add --no-cache wget

# Copy the built JAR from builder stage
COPY --from=builder /app/languagetool-server/target/languagetool-server-*.jar /app/app.jar

# Copy all dependencies
COPY --from=builder /app/languagetool-server/target/lib /app/lib

# Copy server configuration
COPY server-config.properties /app/server-config.properties

# Create combined script to copy JAR and start server
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo '# Copy JAR to /app/target.jar for volume mount (security scanning)' >> /app/start.sh && \
    echo 'cp /app/app.jar /app/target.jar' >> /app/start.sh && \
    echo 'echo "JAR copied to /app/target.jar for security scanning"' >> /app/start.sh && \
    echo '# Build classpath and start server' >> /app/start.sh && \
    echo 'CLASSPATH="/app/app.jar"' >> /app/start.sh && \
    echo 'for jar in /app/lib/*.jar; do CLASSPATH="$CLASSPATH:$jar"; done' >> /app/start.sh && \
    echo '# Check if PUBLIC environment variable is set' >> /app/start.sh && \
    echo 'if [ "$PUBLIC" = "true" ]; then' >> /app/start.sh && \
    echo '  PUBLIC_FLAG="--public"' >> /app/start.sh && \
    echo 'else' >> /app/start.sh && \
    echo '  PUBLIC_FLAG=""' >> /app/start.sh && \
    echo 'fi' >> /app/start.sh && \
    echo 'exec java -cp "$CLASSPATH" org.languagetool.server.HTTPServer $PUBLIC_FLAG --config /app/server-config.properties' >> /app/start.sh && \
    chmod +x /app/start.sh

# Create non-root user for security
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

# Change ownership of the app directory
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the internal port (Prometheus port 9301 remains internal)
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 -O /dev/null http://localhost:8081/v2/languages || exit 1

# Start the LanguageTool server
CMD ["/app/start.sh"]
