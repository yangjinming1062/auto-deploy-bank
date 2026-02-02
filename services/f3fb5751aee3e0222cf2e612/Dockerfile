# Stage 1: Builder
FROM eclipse-temurin:17-jdk as builder

# Install build dependencies
RUN apt-get update -qq && apt-get install -y -qq \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Gradle files and wrapper scripts
COPY build.gradle ./
COPY gradle.properties ./
COPY gradlew ./
COPY gradle/wrapper ./gradle/wrapper

# Make gradlew executable
RUN chmod +x ./gradlew

# Copy source code and build (dependencies will be resolved during build)
COPY src ./src
RUN export GRADLE_USER_HOME=/app/.gradle && ./gradlew shadowJar --no-daemon -x test

# Stage 2: Runtime
FROM eclipse-temurin:17-jre

# Install runtime dependencies
RUN apt-get update -qq && apt-get install -y -qq \
  libuv1 \
  zlib1g \
  libpcre3 \
  libssl3 \
  curl \
  netcat-openbsd \
  socat \
  && rm -rf /var/lib/apt/lists/*

# Create app directory for security scanning volume mount
RUN mkdir -p /app

WORKDIR /opt/mirror

# Copy the built JAR from builder stage to both locations
# /opt/mirror/mirror-all.jar - for running the application
# /app/target.jar - for security scanning volume mount
COPY --from=builder /app/build/libs/*.jar /app/target.jar
COPY --from=builder /app/build/libs/*.jar ./mirror-all.jar

# Copy mirror script from project root
COPY mirror ./

# Copy docker entrypoint
COPY docker/docker-entrypoint.sh ./

# Run user/group setup then exec to java
RUN echo '#!/bin/sh' > ./entrypoint-final && \
    echo 'if ! (getent passwd "$(id -u)" >/dev/null); then useradd -u "$(id -u)" "user$(id -u)"; fi' >> ./entrypoint-final && \
    echo 'if ! (getent group "$(id -g)" >/dev/null); then groupadd -g "$(id -g)" "group$(id -g)"; fi' >> ./entrypoint-final && \
    echo 'exec ./docker-entrypoint.sh "$@"' >> ./entrypoint-final && \
    chmod +x ./entrypoint-final

EXPOSE 49172 8080

CMD ["./entrypoint-final"]