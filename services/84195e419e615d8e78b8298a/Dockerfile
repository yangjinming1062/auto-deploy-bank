# Multi-stage build for FlyCms Spring Boot application

# Stage 1: Build stage
FROM maven:3.6.3-openjdk-8 AS builder

WORKDIR /app

# Copy pom.xml and assembly config first
COPY pom.xml .
COPY assembly.xml .

# Install local dependencies from doc directory
COPY doc/dysmsapi.zip .
RUN unzip -q dysmsapi.zip && \
    mvn install:install-file -Dfile=dysmsapi/alicom-mns-receive-sdk/1.0.1/alicom-mns-receive-sdk-1.0.1.jar \
        -DgroupId=com.alibaba.aliyun.dysmsapi -DartifactId=alicom-mns-receive-sdk -Dversion=1.0.1 -Dpackaging=jar && \
    mvn install:install-file -Dfile=dysmsapi/aliyun-sdk-mns/1.1.8/aliyun-sdk-mns-1.1.8.jar \
        -DgroupId=com.alibaba.aliyun.dysmsapi -DartifactId=aliyun-sdk-mns -Dversion=1.1.8 -Dpackaging=jar && \
    mvn install:install-file -Dfile=dysmsapi/aliyun-java-sdk-core/3.3.1/aliyun-java-sdk-core-3.3.1.jar \
        -DgroupId=com.alibaba.aliyun.dysmsapi -DartifactId=aliyun-java-sdk-core -Dversion=3.3.1 -Dpackaging=jar && \
    mvn install:install-file -Dfile=dysmsapi/aliyun-java-sdk-dysmsapi/1.0.0/aliyun-java-sdk-dysmsapi-1.0.0.jar \
        -DgroupId=com.alibaba.aliyun.dysmsapi -DartifactId=aliyun-java-sdk-dysmsapi -Dversion=1.0.0 -Dpackaging=jar && \
    rm -rf dysmsapi dysmsapi.zip

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine AS flycms

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/FlyCms.jar app.jar

# Expose port 80
EXPOSE 80

# Run the application
CMD ["java", "-jar", "app.jar", "--spring.profiles.active=prod"]

# Stage 3: Export JAR for security scanning
FROM alpine:latest AS exporter
WORKDIR /export
COPY --from=builder /app/target/FlyCms.jar ./target.jar