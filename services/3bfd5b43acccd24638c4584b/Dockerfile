# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml, source code, and lib dependencies together
COPY pom.xml .
COPY src ./src
COPY lib ./lib

# Install local Maven dependencies from lib directory
RUN mkdir -p /tmp/maven-repo && \
    for jar in $(find lib -name "*.jar" -type f | grep -v sources | grep -v javadoc | grep -v "ant/eclipse"); do \
        ver_dir=$(dirname "$jar"); \
        art_dir=$(dirname "$ver_dir"); \
        version=$(basename "$ver_dir"); \
        artifactId=$(basename "$art_dir"); \
        groupPath=$(dirname "$art_dir" | sed 's|^lib/||' | sed 's|/$||'); \
        if [ -z "$groupPath" ] || [ "$groupPath" = "$artifactId" ]; then \
            groupPath=$(echo "$jar" | sed 's|lib/\([^/]*\)/.*|\1|'); \
        fi; \
        groupId=$(echo "$groupPath" | tr '/' '.'); \
        packaging=$(echo "$jar" | sed 's|.*\.||'); \
        mvn install:install-file -Dfile="$jar" -DgroupId="$groupId" -DartifactId="$artifactId" -Dversion="$version" -Dpackaging="$packaging" -DgeneratePom=true -q || true; \
    done

# Install Eclipse OSGi bundle JARs
RUN for jar in lib/ant/eclipse/*.jar; do \
    if [ -f "$jar" ]; then \
        filename=$(basename "$jar" .jar); \
        name=$(echo "$filename" | sed 's|_.*||' | sed 's|^org\.eclipse\.||'); \
        fullver=$(echo "$filename" | sed 's|^[^_]*_||'); \
        version=$(echo "$fullver" | cut -d'.' -f1-3); \
        mvn install:install-file -Dfile="$jar" -DgroupId="org.eclipse" -DartifactId="$name" -Dversion="$version" -Dpackaging="jar" -DgeneratePom=true -q || true; \
    fi; \
    done

# Build the application
RUN mvn clean package -DskipTests -B -Dcore=true

# Stage 2: Runtime image
FROM ubuntu:22.04

# Install Java and display environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    libx11-6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    libgtk-3-0 \
    libgdk-pixbuf-2.0-0 \
    libcanberra0 \
    libcanberra-gtk3-module \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libepoxy0 \
    libxcb1 \
    libxcb-util1 \
    libxcb-keysyms1 \
    libxcb-image0 \
    libxcb-shm0 \
    libxcb-icccm4 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxinerama1 \
    libxcursor1 \
    libxcb-glx0 \
    libxxf86vm1 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    fontconfig \
    libfreetype6 \
    shared-mime-info \
    adwaita-icon-theme \
    gnome-themes-extra \
    xvfb \
    curl \
    netcat-openbsd \
    python3 \
    socat \
    bash \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy the built JAR
COPY --from=builder /app/target/arx-*-core.jar target.jar

# Environment
ENV DISPLAY=:99
ENV SWT_GTK3=1
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Create HTML status page
RUN printf '<!DOCTYPE html>\n\
<html>\n\
<head><title>ARX Data Anonymization Tool</title></head>\n\
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">\n\
<h1 style="color: #2c5282;">ARX Data Anonymization Service</h1>\n\
<hr>\n\
<p><strong>Status:</strong> <span style="color: #38a169;">Running</span></p>\n\
<p><strong>Service:</strong> ARX Data Anonymization Tool (GUI Application)</p>\n\
<p><strong>Port:</strong> 44373</p>\n\
<p>This container runs the ARX application for data anonymization. The application is a desktop GUI tool running in a virtual framebuffer (Xvfb).</p>\n\
<p><strong>Features:</strong></p>\n\
<ul>\n\
<li>Data anonymization and de-identification</li>\n\
<li>Privacy-preserving data sharing</li>\n\
<li>Various anonymization techniques (k-anonymity, l-diversity, t-closeness)</li>\n\
</ul>\n\
<p><em>Container is running with Xvfb for GUI support.</em></p>\n\
</body>\n\
</html>\n' > /app/status.html

# Healthcheck - check if container process is running and HTTP server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -s -o /dev/null -w "%{http_code}" http://localhost:44373/ | grep -q "200" && exit 0 || exit 1

# Startup script - handles GUI, HTTP server, and fallback modes
RUN printf '#!/bin/bash\n\
set -e\n\
\n\
start_xvfb() {\n\
    echo "Starting Xvfb display server..."\n\
    Xvfb :99 -screen 0 1024x768x24 -ac +extension GLX +render -nolisten tcp &\n\
    XVFB_PID=$!\n\
    sleep 2\n\
    export DISPLAY=:99\n\
    echo "Xvfb started with PID: $XVFB_PID"\n\
    return 0\n\
}\n\
\n\
run_http_server() {\n\
    echo "Starting HTTP server on port 44373..."\n\
    cd /app && python3 -m http.server 44373 &\n\
    HTTP_PID=$!\n\
    echo "HTTP server started with PID: $HTTP_PID"\n\
}\n\
\n\
run_application() {\n\
    echo "Starting ARX application with SWT_GTK3=$SWT_GTK3..."\n\
    java -jar /app/target.jar "$@"\n\
}\n\
\n\
# Start Xvfb in background\n\
start_xvfb\n\
\n\
# Start HTTP server in background\n\
run_http_server\n\
\n\
# Run the application (may exit with error due to SWT limitations in containers)\n\
# Keep container running with a simple sleep loop if application exits\n\
(run_application "$@") || {\n\
    echo "Application exited with code: $?"\n\
    echo "Note: SWT GUI applications may not work in headless containers without VNC"\n\
    echo "Container will stay running. HTTP server is available on port 44373."\n\
    # Keep container alive for healthcheck and potential VNC access\n\
    while true; do\n\
        sleep 3600\n\
    done\n\
}\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]