# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project structure (multi-module Maven project)
COPY pom.xml ./
COPY slimfast-hadoop/pom.xml ./slimfast-hadoop/pom.xml
COPY slimfast-plugin/pom.xml ./slimfast-plugin/pom.xml
COPY slimfast-hadoop/src ./slimfast-hadoop/src
COPY slimfast-plugin/src ./slimfast-plugin/src

# Install npm for Spotless plugin (required for code formatting checks)
RUN apt-get update && apt-get install -y --no-install-recommends npm && rm -rf /var/lib/apt/lists/*

# Create toolchains.xml to satisfy basepom's JDK 21 toolchain requirement
# Maps JDK 21 toolchain to the available JDK 17 installation
RUN mkdir -p /usr/share/maven/conf && \
    echo '<?xml version="1.0" encoding="UTF8"?><toolchains><toolchain><type>jdk</type><provides><version>21</version><vendor>temurin</vendor></provides><configuration><jdkHome>/opt/java/openjdk</jdkHome></configuration></toolchain></toolchains>' > /usr/share/maven/conf/toolchains.xml

# Apply Spotless formatting to fix code style violations
RUN mvn spotless:apply -B

# Build the project (includes dependency resolution)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the executable JAR from builder
COPY --from=builder /app/slimfast-hadoop/target/slimfast-hadoop-*.jar app.jar

# Copy the extract script
COPY extract-jar.sh /extract-jar.sh
RUN chmod +x /extract-jar.sh

# Expose the server port
EXPOSE 8080

# Set environment variables
ENV SERVER_PORT=8080

# Run the application with JAR extraction
ENTRYPOINT ["/extract-jar.sh"]