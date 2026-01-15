# Stage 1: Build with Gradle (IntelliJ Platform Plugin)
FROM gradle:9.2.1-jdk21-ubi AS builder

WORKDIR /app

# Copy build configuration files first for better caching
COPY build.gradle.kts settings.gradle.kts gradle.properties ./
COPY gradle/wrapper ./gradle/wrapper

# Copy source code
COPY src ./src
COPY CHANGELOG.md ./

# Add content to empty Unreleased section to satisfy changelog plugin
RUN sed -i '3 a\\n### Added\n\n- Docker build for CI/CD.' CHANGELOG.md || true

# Build the plugin distribution (runs buildPlugin task)
RUN gradle buildPlugin --no-daemon --stacktrace

# Stage 2: Minimal runtime image for artifact extraction
FROM eclipse-temurin:21-jre-alpine AS runtime

WORKDIR /app

# Install nginx for HTTP server
RUN apk add --no-cache nginx wget

# Copy the built plugin from builder stage
COPY --from=builder /app/build/distributions/*.zip /usr/share/nginx/html/target.jar

# Configure nginx and start server
RUN echo 'server { listen 8080; location / { root /usr/share/nginx/html; } }' > /etc/nginx/http.d/default.conf

EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]