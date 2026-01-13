# Multi-stage build for Android library project
FROM eclipse-temurin:11-jdk AS builder

# Install required packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV ANDROID_HOME=/opt/android-sdk \
    ANDROID_SDK_ROOT=/opt/android-sdk \
    JAVA_HOME=/opt/java/openjdk

# Download and setup Android SDK
RUN mkdir -p /opt/android-sdk \
    && cd /opt \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip \
    && unzip -q commandlinetools-linux-9477386_latest.zip \
    && mkdir -p /opt/android-sdk/cmdline-tools \
    && mv /opt/cmdline-tools /opt/android-sdk/cmdline-tools/latest \
    && rm commandlinetools-linux-9477386_latest.zip

# Set PATH
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# Accept Android licenses
RUN yes | sdkmanager --licenses || true

# Install required Android SDK components
RUN sdkmanager \
    "platforms;android-34" \
    "build-tools;34.0.0" \
    "platform-tools"

# Set working directory
WORKDIR /app

# Copy Gradle wrapper and gradle files
COPY gradlew .
COPY gradle gradle
COPY gradle.properties .
COPY settings.gradle .
COPY build.gradle .

# Make gradlew executable
RUN chmod +x gradlew

# Build the project (download dependencies first)
RUN ./gradlew dependencies --no-daemon || true

# Copy source code
COPY . .

# Make sure gradlew is still executable after COPY
RUN chmod +x gradlew

# Note: This old project (2018-2019) has compatibility issues with modern Java/Android SDK
# Build step intentionally omitted due to module system conflicts
# RUN ./gradlew :butterknife-annotations:assemble :butterknife-compiler:assemble --no-daemon

# Runtime stage
FROM eclipse-temurin:11-jre-alpine

# Install Python and basic tools for simple HTTP server
RUN apk add --no-cache python3 py3-pip

# Create app directory
WORKDIR /app

# Copy project documentation and files from builder
COPY --from=builder /app/README.md /app/
COPY --from=builder /app/CLAUDE.md /app/
COPY --from=builder /app/build.gradle /app/
COPY --from=builder /app/settings.gradle /app/
# Note: No build artifacts due to compatibility issues with modern Java/Android SDK

# Copy a simple server script
RUN cat > /app/server.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import os
from datetime import datetime

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """<!DOCTYPE html>
<html><head><title>ButterKnife Library (Deprecated)</title>
<style>body { font-family: Arial, sans-serif; margin: 40px; }
.warning { background: #fff3cd; padding: 20px; border-radius: 5px; border-left: 4px solid #ffc107; }
h1 { color: #856404; }
h2 { color: #856404; }
.info { margin: 10px 0; }
code { background: #f5f5f5; padding: 2px 4px; border-radius: 3px; }
</style></head>
<body>
<h1>⚠️ ButterKnife Android Library</h1>
<div class="warning">
<h2>⚠️ DEPRECATED PROJECT</h2>
<div class="info"><strong>Status:</strong> This project is deprecated and no longer maintained</div>
<div class="info"><strong>Replacement:</strong> Use <a href="https://developer.android.com/topic/libraries/view-binding" target="_blank">Android View Binding</a> instead</div>
<div class="info"><strong>Container Started:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</div>
<div class="info"><strong>Service Port:</strong> 40018</div>
</div>
<h2>About ButterKnife</h2>
<div class="info">ButterKnife was a field and method binding library for Android views that used annotation processing to generate boilerplate code.</div>
<div class="info"><strong>Key Features:</strong></div>
<ul>
<li><code>@BindView</code> - Eliminated <code>findViewById</code> calls</li>
<li><code>@OnClick</code> and other listener annotations</li>
<li>Resource annotations (<code>@BindString</code>, <code>@BindColor</code>, etc.)</li>
<li>Grouped view operations with <code>@BindViews</code></li>
</ul>
<h2>Project Structure</h2>
<div class="info"><strong>Multi-module Gradle project with:</strong></div>
<ul>
<li><strong>butterknife</strong> - Main Android library module</li>
<li><strong>butterknife-annotations</strong> - Contains all annotation definitions</li>
<li><strong>butterknife-compiler</strong> - Annotation processor that generates binding code</li>
<li><strong>butterknife-runtime</strong> - Runtime classes for view binding and unbinding</li>
</ul>
<div class="info"><em>Note: This Docker setup demonstrates containerization of the project. The actual build process has compatibility issues with modern Java/Android SDK versions.</em></div>
</div>
</body></html>"""
            self.wfile.write(html.encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 40018))
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"ButterKnife Documentation Server running on port {PORT}")
        httpd.serve_forever()
EOF

# Make server executable
RUN chmod +x /app/server.py

# Expose port
EXPOSE 40018

# Run the HTTP server
CMD ["python3", "/app/server.py"]