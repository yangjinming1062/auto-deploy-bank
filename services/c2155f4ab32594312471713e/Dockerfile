# Multi-stage build for Gradle 9.4.0
# Stage 1: Build the Gradle distribution
FROM eclipse-temurin:17-jdk AS builder

WORKDIR /build

# Install necessary tools for building
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Gradle wrapper and build files
COPY gradlew ./
COPY gradle/ ./gradle/
COPY build.gradle.kts ./
COPY settings.gradle.kts ./
COPY gradle.properties ./
COPY version.txt ./
COPY released-versions.json ./
COPY packaging/ ./packaging/
COPY platforms/ ./platforms/
COPY subprojects/ ./subprojects/
COPY build-logic/ ./build-logic/
COPY build-logic-commons/ ./build-logic-commons/
COPY build-logic-settings/ ./build-logic-settings/
COPY architecture/ ./architecture/
COPY contributing/ ./contributing/
COPY testing/ ./testing/

# Make Gradle wrapper executable
RUN chmod +x gradlew

# Build the full Gradle distribution
# This creates an installable distribution in build/install
RUN ./gradlew installAll -x test -Pgradle_installPath=/build/installAll --no-daemon

# Stage 2: Create minimal runtime image
FROM eclipse-temurin:17-jre-alpine

# Install bash, python3, and wget for script support, web server, and healthchecks
RUN apk add --no-cache bash python3 wget

WORKDIR /opt/gradle

# Copy the built Gradle distribution from builder stage
COPY --from=builder /build/installAll distribution

# Set up the Gradle installation
RUN mv distribution gradle-home

# Create a symlink for convenience
RUN ln -s /opt/gradle/gradle-home/bin/gradle /usr/local/bin/gradle

# Set environment variables
ENV GRADLE_HOME=/opt/gradle/gradle-home
ENV PATH=$GRADLE_HOME/bin:$PATH

# Create working directory
WORKDIR /workspace

# Create a web root directory and copy the target.jar
RUN mkdir -p /webroot
COPY target.jar /webroot/target.jar

# Create an index.html for the web service
RUN echo '<html><head><title>Gradle Distribution Service</title></head><body><h1>Gradle Distribution Service</h1><p>Service is running on port 40096</p><p>This is a Gradle build automation service.</p><p><a href="/target.jar">Download Gradle Wrapper JAR</a></p></body></html>' > /webroot/index.html

# Default command - serve files via Python HTTP server
CMD ["python3", "-m", "http.server", "40096", "--directory", "/webroot"]