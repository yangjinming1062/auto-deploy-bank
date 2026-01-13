# Multi-stage build for iText Core Community
# Stage 1: Build the project
FROM maven:3.9-eclipse-temurin-17 AS builder

# Install Ghostscript and ImageMagick for tests
RUN apt-get update && \
    apt-get install -y \
    ghostscript \
    imagemagick && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy pom.xml and source code
COPY pom.xml .
COPY . .

# Copy web service source
COPY WebService.java /build/WebService.java

# Build the project (skip tests for faster build)
RUN mvn clean install -Dmaven.test.skip=true -B

# Compile web service
RUN javac /build/WebService.java

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre

# Set working directory
WORKDIR /app

# Copy built JARs from builder stage
COPY --from=builder /build/layout/target/itext-layout-*.jar /app/itext-layout.jar
COPY --from=builder /build/kernel/target/itext-kernel-*.jar /app/itext-kernel.jar

# Copy compiled web service (including inner classes)
COPY --from=builder /build/WebService*.class /app/

# Copy environment variables
ENV ITEXT_GS_EXEC=gs
ENV ITEXT_MAGICK_COMPARE_EXEC="magick compare"
ENV JAVA_OPTS=-Xmx1024m

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose port 40133
EXPOSE 40133

# Start the web service
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]