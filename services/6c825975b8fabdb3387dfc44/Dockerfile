# Stage 1: Build with Gradle
FROM gradle:7.6-jdk17 AS builder

WORKDIR /app

# Create source directory
RUN mkdir -p /app/src/main/java/comsat/sample/actuator
RUN mkdir -p /app/src/main/resources

# Create a minimal Spring Boot application
RUN cat > /app/src/main/java/comsat/sample/actuator/SampleActuatorApplication.java << 'EOF'
package comsat.sample.actuator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SampleActuatorApplication {
    public static void main(String[] args) throws Exception {
        SpringApplication.run(SampleActuatorApplication.class, args);
    }
}
EOF

# Copy application.properties
RUN cat > /app/src/main/resources/application.properties << 'EOF'
logging.file: /tmp/logs/app.log
logging.level.org.springframework.security: INFO
management.address: 127.0.0.1
endpoints.shutdown.enabled: true
server.tomcat.basedir: target/tomcat
server.tomcat.access_log_enabled: true
server.tomcat.access_log_pattern: %h %t "%r" %s %b
EOF

# Create a minimal build.gradle
RUN cat > /app/build.gradle << 'EOF'
plugins {
    id 'java'
    id 'org.springframework.boot' version '2.7.18'
    id 'io.spring.dependency-management' version '1.0.15.RELEASE'
}

repositories {
    mavenCentral()
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

dependencies {
    implementation "org.springframework.boot:spring-boot-starter-actuator"
    implementation "org.springframework.boot:spring-boot-starter-web"
}
EOF

# Build the project
RUN gradle bootJar -x test --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/build/libs/*.jar app.jar

# Create a startup script
COPY <<'EOF' /entrypoint.sh
#!/bin/sh
sleep 3
# Copy JAR to the mounted volume path for security scanning
cp /app/app.jar /app/target.jar
exec java -jar /app/app.jar
EOF
RUN chmod +x /entrypoint.sh

# Expose default Spring Boot port (8080)
EXPOSE 8080

# Run the application
ENTRYPOINT ["/entrypoint.sh"]