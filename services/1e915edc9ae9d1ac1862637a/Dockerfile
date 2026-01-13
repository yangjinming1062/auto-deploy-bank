# Multi-stage build for Grails Framework
# Stage 1: Build stage
FROM eclipse-temurin:8-jdk AS builder

# Install wget, ca-certificates, and unzip for SSL and archive extraction
RUN apt-get update && apt-get install -y wget ca-certificates unzip && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Install Gradle 6.9.1
RUN wget https://services.gradle.org/distributions/gradle-6.9.1-bin.zip && \
    unzip gradle-6.9.1-bin.zip && \
    mv gradle-6.9.1 /opt/gradle && \
    ln -s /opt/gradle/bin/gradle /usr/bin/gradle

# Copy Gradle wrapper and build files
COPY gradle.properties .
COPY settings.gradle .
COPY build.gradle .
COPY gradle/ ./gradle/

# Copy source code
COPY . .

# Grant execute permission to gradlew (if present)
RUN if [ -f ./gradlew ]; then chmod +x ./gradlew; fi

# Set environment variables for build
ENV GRADLE_OPTS="-Xmx2G -Xms2G -XX:NewSize=512m -XX:MaxNewSize=512m"
ENV JAVA_OPTS="-Xmx2G"
ENV PATH="/opt/gradle/bin:$PATH"

# Build and install the Grails framework
# Using --no-daemon to avoid daemon issues in containers
RUN gradle install --no-daemon

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre AS runtime

# Install Python3 for simple HTTP server
RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed Grails from builder stage
# The install task creates dist/ and lib/ directories
COPY --from=builder /build/dist ./dist
COPY --from=builder /build/lib ./lib
COPY --from=builder /build/bin ./bin
COPY --from=builder /build/grails-bootstrap/build/libs/grails-bootstrap-5.0.2-SNAPSHOT.jar ./lib/
COPY --from=builder /build/grails-shell/build/libs/grails-shell-5.0.2-SNAPSHOT.jar ./lib/

# Copy JAR bundling script
COPY bundle-jars.sh /tmp/bundle-jars.sh
RUN chmod +x /tmp/bundle-jars.sh && /tmp/bundle-jars.sh

# Copy web server script
COPY web-server.sh /tmp/web-server.sh
RUN chmod +x /tmp/web-server.sh

# Create target.jar as a copy of grails-shell JAR for security scanning
RUN cp /app/lib/grails-shell-5.0.2-SNAPSHOT.jar /app/target.jar

# Set environment variables
ENV GRAILS_HOME=/app
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=$GRAILS_HOME/bin:$PATH
ENV GRADLE_OPTS="-Xmx2G -Xms2G -XX:NewSize=512m -XX:MaxNewSize=512m"
ENV PORT=40597

# Expose port 40597
EXPOSE 40597

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:40597/ || exit 1

# Run web server to serve Grails framework information
CMD ["/tmp/web-server.sh"]