# Stage 1: Build with Gradle
FROM gradle:8.5-jdk17 AS builder

WORKDIR /build

# Copy build configuration files
COPY build.gradle .
COPY src ./src

# Build the WAR file
RUN gradle clean war -x test --no-daemon

# Stage 2: Runtime with Open Liberty
FROM open-liberty:full-java17-openj9

# Copy server configuration
COPY --chown=1001:0 server.xml bootstrap.properties server.env jvm.options /config/

# Copy WAR file from builder stage to Liberty dropins directory
COPY --chown=1001:0 --from=builder /build/build/libs/myapp.war /config/dropins/myapp.war

# Copy WAR file for security scanner (mounted at /tmp/app.jar in compose)
# Renamed to target.jar as required by security scanner
COPY --chown=1001:0 --from=builder /build/build/libs/myapp.war /tmp/target.jar

# Expose HTTP port (9080) and HTTPS port (9443)
EXPOSE 9080 9443

# Use default entrypoint which runs server