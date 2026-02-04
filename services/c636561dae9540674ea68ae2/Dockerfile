# Stage 1: Build with Gradle 7.3.3 and Java 11
FROM gradle:7.3.3-jdk11 AS builder

WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle settings.gradle gradle.properties ./
COPY mybatis-plus-boot-starter-test/build.gradle ./mybatis-plus-boot-starter-test/
COPY mybatis-plus-boot-starter/build.gradle ./mybatis-plus-boot-starter/
COPY mybatis-plus/build.gradle ./mybatis-plus/
COPY mybatis-plus-core/build.gradle ./mybatis-plus-core/
COPY mybatis-plus-annotation/build.gradle ./mybatis-plus-annotation/
COPY mybatis-plus-extension/build.gradle ./mybatis-plus-extension/

# Copy source code
COPY . .

# Build the shadow jar (skip tests for faster builds)
RUN gradle :mybatis-plus-boot-starter-test:shadowJar -x test --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:11-jre-alpine

WORKDIR /home/ubuntu/deploy-projects/c636561dae9540674ea68ae2

# Copy the built shadow JAR from builder stage
COPY --from=builder /build/mybatis-plus-boot-starter-test/build/libs/target.jar app.jar

# Expose the port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]