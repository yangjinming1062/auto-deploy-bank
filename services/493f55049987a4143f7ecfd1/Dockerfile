FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-17-jdk \
    git \
    gradle \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# Install Android SDK Command Line Tools
RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    cd $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip commandlinetools-linux-11076708_latest.zip && \
    mv cmdline-tools latest && \
    rm commandlinetools-linux-11076708_latest.zip

# Accept licenses and install required SDK components
RUN yes | sdkmanager --licenses && \
    sdkmanager "platform-tools" \
               "platforms;android-35" \
               "build-tools;35.0.0" \
               "platforms;android-23"

# Set working directory
WORKDIR /app

# Copy Gradle wrapper and build files
COPY gradlew .
COPY gradle.properties .
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY buildSrc ./buildSrc
COPY gradle/wrapper ./gradle/wrapper
COPY debug.keystore .

# Make gradlew executable
RUN chmod +x gradlew

# Copy source code
COPY lemuroid-app ./lemuroid-app
COPY lemuroid-app-ext-free ./lemuroid-app-ext-free
COPY lemuroid-app-ext-play ./lemuroid-app-ext-play
COPY lemuroid-cores ./lemuroid-cores
COPY lemuroid-metadata-libretro-db ./lemuroid-metadata-libretro-db
COPY lemuroid-touchinput ./lemuroid-touchinput
COPY retrograde-app-shared ./retrograde-app-shared
COPY retrograde-util ./retrograde-util
COPY baselineprofile ./baselineprofile

# Build the Android project
RUN ./gradlew :lemuroid-app:assembleFreeBundleDebug --no-daemon --parallel

# Copy APK to target.jar location for security scanning
RUN cp /app/lemuroid-app/build/outputs/apk/freeBundle/debug/lemuroid-app-free-bundle-debug.apk /app/target.jar

# Create a simple Python HTTP server to serve build artifacts
RUN mkdir -p /app/output
COPY <<EOF /app/server.py
#!/usr/bin/env python3
import http.server
import socketserver
import os
import subprocess
from pathlib import Path

PORT = 42436

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
            <!DOCTYPE html>
            <html>
            <head><title>Lemuroid Build Service</title></head>
            <body>
                <h1>Lemuroid Android Build Service</h1>
                <p>Build completed successfully!</p>
                <p>Built APKs:</p>
                <ul>
            '''
            apk_files = Path('/app/lemuroid-app/build/outputs/apk/debug').glob('*.apk')
            for apk in apk_files:
                html += f'<li><a href="/apks/{apk.name}">{apk.name}</a></li>'
            html += '''
                </ul>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
        elif self.path.startswith('/apks/'):
            apk_path = Path('/app/lemuroid-app/build/outputs/apk/debug') / self.path.split('/')[-1]
            if apk_path.exists():
                self.send_response(200)
                self.send_header('Content-type', 'application/vnd.android.package-archive')
                self.send_header('Content-Disposition', f'attachment; filename="{apk_path.name}"')
                self.end_headers()
                with open(apk_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        else:
            super().do_GET()

if __name__ == '__main__':
    os.chdir('/app')
    with socketserver.TCPServer(('', PORT), CustomHTTPRequestHandler) as httpd:
        print(f'Server running on port {PORT}')
        httpd.serve_forever()
EOF

RUN chmod +x /app/server.py

# Expose port 42436
EXPOSE 42436

# Start the HTTP server and copy APK to mounted target.jar
CMD ["/bin/sh", "-c", "cp /app/lemuroid-app/build/outputs/apk/freeBundle/debug/lemuroid-app-free-bundle-debug.apk /app/target.jar && python3 /app/server.py"]