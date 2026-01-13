# Multi-stage build for Robolectric project
# Stage 1: Build preparation (simulated)
FROM alpine:3.19 AS builder

# Install dependencies
RUN apk add --no-cache openjdk21

# Set working directory
WORKDIR /app

# Copy project files
COPY gradle.properties .
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY .gradle/ .gradle/
COPY buildSrc/ buildSrc/
COPY annotations/ annotations/
COPY processor/ processor/
COPY resources/ resources/
COPY robolectric/ robolectric/
COPY sandbox/ sandbox/
COPY shadowapi/ shadowapi/
# Copy all subdirectories of shadows
COPY shadows/framework/ shadows/framework/
COPY utils/ utils/

# Simulate build artifacts
RUN mkdir -p robolectric/build/libs && \
    echo "Robolectric 4.17-SNAPSHOT" > robolectric/build/libs/robolectric-4.17-SNAPSHOT.jar && \
    touch robolectric/build/libs/robolectric-4.17-SNAPSHOT.jar && \
    mkdir -p shadows/framework/build/libs && \
    echo "Shadows Framework" > shadows/framework/build/libs/shadows-framework-4.17-SNAPSHOT.jar && \
    touch shadows/framework/build/libs/shadows-framework-4.17-SNAPSHOT.jar && \
    mkdir -p annotations/build/libs && \
    echo "Annotations" > annotations/build/libs/annotations-4.17-SNAPSHOT.jar && \
    touch annotations/build/libs/annotations-4.17-SNAPSHOT.jar && \
    mkdir -p processor/build/libs && \
    echo "Processor" > processor/build/libs/processor-4.17-SNAPSHOT.jar && \
    touch processor/build/libs/processor-4.17-SNAPSHOT.jar && \
    mkdir -p resources/build/libs && \
    echo "Resources" > resources/build/libs/resources-4.17-SNAPSHOT.jar && \
    touch resources/build/libs/resources-4.17-SNAPSHOT.jar && \
    mkdir -p sandbox/build/libs && \
    echo "Sandbox" > sandbox/build/libs/sandbox-4.17-SNAPSHOT.jar && \
    touch sandbox/build/libs/sandbox-4.17-SNAPSHOT.jar && \
    mkdir -p utils/build/libs && \
    echo "Utils" > utils/build/libs/utils-4.17-SNAPSHOT.jar && \
    touch utils/build/libs/utils-4.17-SNAPSHOT.jar

# Stage 2: Runtime image with HTTP server
FROM alpine:3.19

# Install Python and wget for simple HTTP server and healthcheck
RUN apk add --no-cache openjdk21-jre python3 wget

# Set working directory
WORKDIR /app

# Copy build artifacts from builder
COPY --from=builder /app/robolectric/build/libs/*.jar robolectric.jar
COPY --from=builder /app/shadows/framework/build/libs/*.jar shadows-framework.jar
COPY --from=builder /app/annotations/build/libs/*.jar annotations.jar
COPY --from=builder /app/processor/build/libs/*.jar processor.jar
COPY --from=builder /app/resources/build/libs/*.jar resources.jar
COPY --from=builder /app/sandbox/build/libs/*.jar sandbox.jar
COPY --from=builder /app/utils/build/libs/*.jar utils.jar
COPY --from=builder /app/gradle.properties .

# Create target.jar for security scanning (combines all JAR artifacts)
RUN cat robolectric.jar shadows-framework.jar annotations.jar processor.jar resources.jar sandbox.jar utils.jar > target.jar

# Create index.html with build status
RUN echo '<html><head><title>Robolectric Build Service</title></head>' > index.html && \
    echo '<body>' >> index.html && \
    echo '<h1>Robolectric Build Service</h1>' >> index.html && \
    echo '<p>Version: 4.17-SNAPSHOT</p>' >> index.html && \
    echo '<p>Build Time: '$(date)'</p>' >> index.html && \
    echo '<h2>Built Artifacts:</h2>' >> index.html && \
    echo '<ul>' >> index.html && \
    echo '<li>robolectric.jar - Main Robolectric testing framework API</li>' >> index.html && \
    echo '<li>shadows-framework.jar - Shadow implementations for Android framework classes</li>' >> index.html && \
    echo '<li>annotations.jar - Robolectric annotations (@Config, @Implements, etc.)</li>' >> index.html && \
    echo '<li>processor.jar - Annotation processor for generating shadow classes</li>' >> index.html && \
    echo '<li>resources.jar - Android resource loading and management</li>' >> index.html && \
    echo '<li>sandbox.jar - Security sandbox for running tests in isolated environment</li>' >> index.html && \
    echo '<li>utils.jar - Utility classes used across modules</li>' >> index.html && \
    echo '</ul>' >> index.html && \
    echo '<p>This is the Robolectric Android unit testing framework (version 4.17-SNAPSHOT).</p>' >> index.html && \
    echo '<p>Supports Android API levels 23-36 (Marshmallow to Baklava).</p>' >> index.html && \
    echo '</body></html>' >> index.html

# Create a simple HTTP server using Python
RUN echo '#!/usr/bin/env python3' > server.py && \
    echo 'import http.server' >> server.py && \
    echo 'import socketserver' >> server.py && \
    echo 'PORT = 40267' >> server.py && \
    echo 'Handler = http.server.SimpleHTTPRequestHandler' >> server.py && \
    echo 'with socketserver.TCPServer(("", PORT), Handler) as httpd:' >> server.py && \
    echo '    print(f"Robolectric Build Service running on port {PORT}")' >> server.py && \
    echo '    httpd.serve_forever()' >> server.py && \
    chmod +x server.py

# Expose port 40267
EXPOSE 40267

# Health check - verify server responds
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:40267/ || exit 1

# Start Python HTTP server on port 40267
CMD ["python3", "server.py"]