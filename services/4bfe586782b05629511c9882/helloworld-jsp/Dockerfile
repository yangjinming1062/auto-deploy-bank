# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source files
COPY src ./src

# Build the WAR file
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image with Jetty
FROM eclipse-temurin:17-jre-alpine

# Download Jetty Runner
ENV JETTY_VERSION=9.4.54.v20240208

RUN mkdir -p /opt/jetty && \
    apk add --no-cache bash wget && \
    rm -rf /var/cache/apk/* && \
    wget -q -O /opt/jetty/jetty-runner.jar https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-runner/${JETTY_VERSION}/jetty-runner-${JETTY_VERSION}.jar

# Copy the built WAR from builder stage
COPY --from=builder /app/target/helloworld-jsp-1.0-SNAPSHOT.war /opt/jetty/ROOT.war
# Copy for security scanning (named target.jar as required)
COPY --from=builder /app/target/helloworld-jsp-1.0-SNAPSHOT.war /app/target.jar

# Expose the default Jetty port
EXPOSE 8080

# Run Jetty with the WAR file
CMD ["java", "-jar", "/opt/jetty/jetty-runner.jar", "--port", "8080", "/opt/jetty/ROOT.war"]