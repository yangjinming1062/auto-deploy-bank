# Multi-stage Dockerfile for IntelliJ Platform Plugin (Ijaas)
# Stage 1: Build the plugin using Gradle
FROM gradle:8.0-jdk17 AS builder

WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle .
COPY gradle/wrapper/gradle-wrapper.properties gradle/wrapper/
# Copy source files
COPY resources/META-INF/plugin.xml src/main/resources/META-INF/
COPY src src/

# Build the plugin (produces a ZIP in build/distributions)
RUN gradle buildPlugin --no-daemon -q

# Stage 2: Runtime image with IntelliJ IDEA headless
# Use Java 11 as IntelliJ 2021.3 bundles JBR 11 and is designed for Java 11
# Use non-Alpine image because JBR requires glibc (not musl used by Alpine)
FROM eclipse-temurin:11-jdk

# Install dependencies for IntelliJ headless operation
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    zip \
    libxrender1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libfontconfig1 \
    libfreetype6 \
    libncurses6 \
    bash \
    coreutils \
    net-tools \
    xvfb \
    python3 \
    libnsl2 \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables - use JBR bundled with IntelliJ
ENV JAVA_HOME=/opt/intellij/jbr
ENV IDEA_HOME=/opt/intellij
ENV IJAAS_PORT=5800
ENV AWT_HEADLESS=true
ENV DISPLAY=:99
ENV XAUTHORITY=/tmp/.Xauthority

# Download and install IntelliJ IDEA Community Edition (headless)
RUN wget -q -O /tmp/idea.tar.gz https://download.jetbrains.com/idea/ideaIC-2021.3.3.tar.gz && \
    mkdir -p /opt/intellij && \
    tar -xzf /tmp/idea.tar.gz -C /opt/intellij --strip-components=1 && \
    rm /tmp/idea.tar.gz && \
    mkdir -p /opt/intellij.plugins/homebrew/.IntelliJIdea/config/plugins

# Copy the built plugin from builder stage
COPY --from=builder /build/build/distributions/*.zip /tmp/plugin.zip
COPY --from=builder /build/src/main/resources/META-INF/plugin.xml /tmp/plugin.xml

# Create app directory and extract plugin with proper structure
RUN mkdir -p /app /build-output && \
    cd /tmp && \
    rm -rf build-temp && \
    unzip -q plugin.zip -d build-temp && \
    PLUGIN_DIR=/opt/intellij.plugins/homebrew/.IntelliJIdea/config/plugins/ijaas-0.1 && \
    mkdir -p $PLUGIN_DIR/lib $PLUGIN_DIR/META-INF && \
    # Copy lib files (handle nested build directory structure)
    cp -r build-temp/build/lib/* $PLUGIN_DIR/lib/ 2>/dev/null || \
    cp -r build-temp/lib/* $PLUGIN_DIR/lib/ 2>/dev/null || \
    cp -r build-temp/* $PLUGIN_DIR/lib/ 2>/dev/null || true && \
    # Copy plugin.xml
    cp /tmp/plugin.xml $PLUGIN_DIR/META-INF/ && \
    # Create target.jar in /app for security scanning
    cd $PLUGIN_DIR && zip -q -r /app/target.jar . && \
    cp /app/target.jar /build-output/target.jar && \
    rm -rf /tmp/plugin.zip /tmp/plugin.xml build-temp

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the HTTP bridge port (5800) and internal TCP server port (5801)
EXPOSE 5800 5801

# Copy HTTP bridge
COPY http_bridge.py /http_bridge.py

# Run IntelliJ in headless mode with Xvfb virtual display
# The plugin's IjaasStartupActivity will start the TCP server when IntelliJ initializes
# IjaasServer runs on port 5801 (internal), HTTP bridge runs on port 5800 (external)
WORKDIR /opt/intellij

ENTRYPOINT ["/entrypoint.sh"]
CMD ["sleep", "infinity"]