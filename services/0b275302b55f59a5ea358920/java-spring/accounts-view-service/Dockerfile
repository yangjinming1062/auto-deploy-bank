# Multi-stage build for Accounts View Service
FROM eclipse-temurin:8-jdk AS builder
WORKDIR /project
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*
# Install Gradle 2.14.1 - compatible with Spring Boot 1.3.5 and Java 8
RUN wget -q https://services.gradle.org/distributions/gradle-2.14.1-bin.zip && \
    unzip -q gradle-2.14.1-bin.zip && rm gradle-2.14.1-bin.zip
ENV PATH=$PATH:/project/gradle-2.14.1/bin
# Copy entire project
COPY . .
# Build
RUN gradle :accounts-view-service:assemble --no-daemon

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
USER app
COPY --from=builder /project/accounts-view-service/build/libs/*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]