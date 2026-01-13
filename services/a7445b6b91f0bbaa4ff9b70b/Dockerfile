# Multi-stage build for Spring Cloud Gateway
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-8 AS builder

ARG SERVICE_MODULE=mss-gateway

WORKDIR /app

# Copy pom.xml and pom files for all modules
COPY pom.xml .
COPY mss-common/pom.xml mss-common/
COPY mss-gateway/pom.xml mss-gateway/
COPY mss-oauth/pom.xml mss-oauth/
COPY mss-upms/pom.xml mss-upms/
COPY mss-monitor/pom.xml mss-monitor/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY mss-common/src mss-common/src
COPY mss-gateway/src mss-gateway/src
COPY mss-oauth/src mss-oauth/src
COPY mss-upms/src mss-upms/src
COPY mss-monitor/src mss-monitor/src

# Build all modules
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM amazoncorretto:8

WORKDIR /app

ARG SERVICE_MODULE=mss-gateway

# Copy the built JAR from builder stage
COPY --from=builder /app/${SERVICE_MODULE}/target/*.jar target.jar

EXPOSE 9030

CMD ["java", "-jar", "target.jar"]