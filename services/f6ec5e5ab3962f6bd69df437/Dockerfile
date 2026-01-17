# Multi-stage build for IQQ desktop QQ client
# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy source code and libraries
COPY . .

# Install local libraries to Maven repository
RUN mvn install:install-file -Dfile=main/lib/webqq-core-1.2-SNAPSHOT.jar -DgroupId=iqq.im -DartifactId=webqq-core -Dversion=1.2-SNAPSHOT -Dpackaging=jar && \
    mvn install:install-file -Dfile=main/lib/weblaf-1.29.jar -DgroupId=weblaf -DartifactId=weblaf -Dversion=1.29 -Dpackaging=jar && \
    mvn install:install-file -Dfile=main/lib/jhrome-2.0.jar -DgroupId=Jhrome -DartifactId=Jhrome -Dversion=2.0 -Dpackaging=jar && \
    mvn install:install-file -Dfile=main/lib/iqq-bridge-webqq-3.0.0-SNAPSHOT.jar -DgroupId=iqq.app -DartifactId=iqq-bridge-webqq -Dversion=3.0.0-SNAPSHOT -Dpackaging=jar

# Build the project
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM alpine:latest

# Install Java, Xvfb, X11 graphics libraries, and noVNC dependencies
RUN apk add --no-cache \
    openjdk8-jre \
    xvfb \
    ttf-dejavu \
    fontconfig \
    dbus \
    udev \
    bash \
    xorg-server \
    xrandr \
    mesa-gl \
    mesa-dri-gallium \
    libxrender \
    libxext \
    libxi \
    libxtst \
    git \
    python3 \
    py3-pip \
    npm \
    nodejs \
    websockify

# Install Python websockets package for noVNC server
RUN pip3 install --break-system-packages websockets

# Create app directory
WORKDIR /app

# Copy the built JAR and startup script from builder stage
COPY --from=builder /app/main/target/iqq-main-3.0.0-SNAPSHOT-jar-with-dependencies.jar /app/target.jar
COPY start.sh /start.sh
COPY novnc_server.py /app/novnc_server.py
RUN chmod +x /start.sh /app/novnc_server.py

# Clone noVNC for web-based remote desktop access
RUN git clone https://github.com/novnc/noVNC.git /app/noVNC && \
    chmod +x /app/noVNC/utils/novnc_proxy

# Expose ports: 40432 for original app, 6080 for noVNC web interface
EXPOSE 40432 6080

# Set display environment variable for headless operation
ENV DISPLAY=:99

# Add volume mount for security scanning
VOLUME ["/app/target.jar"]

# Start the application with Xvfb
CMD ["/start.sh"]