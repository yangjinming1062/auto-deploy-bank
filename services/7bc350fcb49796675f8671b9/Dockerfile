# Root Dockerfile that delegates to core/Dockerfile
# This file is for security scanning - actual build uses core/Dockerfile

FROM eclipse-temurin:17-jre-alpine

# Copy the pre-built JAR from the core module
COPY core/target/reverb-core-*-jar-with-dependencies.jar target.jar

EXPOSE 42122

CMD ["java", "-jar", "target.jar"]