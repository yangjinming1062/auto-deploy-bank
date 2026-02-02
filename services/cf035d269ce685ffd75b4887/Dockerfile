# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first
COPY pom.xml .

# Copy source code and resources
COPY src ./src

# Build the WAR package (dependencies will be downloaded during build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime with Jetty on Debian
FROM eclipse-temurin:8-jre-alpine

# Set timezone
ENV TZ=Asia/Shanghai

# Install LibreOffice for document conversion (JodConverter)
RUN apk add --no-cache libreoffice-writer curl

# Set LibreOffice home path
ENV OFFICE_HOME=/usr/lib/libreoffice

# Copy Jetty runner
RUN mkdir -p /var/lib/jetty/webapps && \
    curl -L -o /var/lib/jetty/jetty-runner.jar https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-runner/9.4.58.v20250814/jetty-runner-9.4.58.v20250814.jar

# Copy the WAR file from builder
COPY --from=builder /app/target/lib.war /var/lib/jetty/webapps/ROOT.war

# Copy target.jar for security scanning
COPY --from=builder /app/target/lib.war /app/target.jar

# Expose the default Jetty port
EXPOSE 8080

# Run with Jetty runner
CMD ["java", "-jar", "/var/lib/jetty/jetty-runner.jar", "/var/lib/jetty/webapps/ROOT.war"]