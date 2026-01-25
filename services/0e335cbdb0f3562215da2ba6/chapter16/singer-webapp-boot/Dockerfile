# Stage 1: Build with Gradle (use JDK11 for compatibility with Gradle 6.9 and older Spring)
FROM gradle:6.9.4-jdk11 AS builder

WORKDIR /app

# Copy entire project structure (required for Gradle multi-module validation)
COPY . .

# Patch the SingerApplication to not close the context (keep running in Docker)
RUN sed -i 's/ctx.close();/\/\/ ctx.close(); \/\/ Disabled for Docker/' chapter16/singer-webapp-boot/src/main/java/com/apress/prospring5/ch16/SingerApplication.java

# Create init script to fix repository issues - use HTTPS URLs
RUN printf 'allprojects {\n    repositories {\n        mavenCentral()\n        maven { url "https://repo.spring.io/snapshot" }\n        maven { url "https://repo.spring.io/release" }\n    }\n    buildscript {\n        repositories {\n            mavenCentral()\n            maven { url "https://repo.spring.io/snapshot" }\n            maven { url "https://repo.spring.io/release" }\n        }\n    }\n}\n' > init.gradle

# Build only the singer-webapp-boot module with init script
RUN gradle :chapter16:singer-webapp-boot:clean :chapter16:singer-webapp-boot:bootJar -x test --no-daemon --init-script init.gradle

# Stage 2: Runtime image
FROM eclipse-temurin:17-jdk-alpine

# Install curl and bash for health checks and scripts
RUN apk add --no-cache curl bash

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/chapter16/singer-webapp-boot/build/libs/*.jar app.jar

# Expose the application port
EXPOSE 8080

# Create a custom entry point that properly runs Spring Boot
# Simple run script since ctx.close() is now disabled
RUN printf '#!/bin/bash\nexec java --add-opens=java.base/java.lang=ALL-UNNAMED \\\n     --add-opens=java.base/java.lang.invoke=ALL-UNNAMED \\\n     --add-opens=java.base/java.util=ALL-UNNAMED \\\n     -jar app.jar\n' > run.sh && chmod +x run.sh

# Run the application
CMD ["./run.sh"]