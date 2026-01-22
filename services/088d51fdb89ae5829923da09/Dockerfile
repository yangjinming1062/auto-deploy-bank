# Stage 1: Build with Gradle
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /project

# Copy Spring Boot project files
COPY example-projects/spring-boot/gradlew .
COPY example-projects/spring-boot/gradle ./gradle
COPY example-projects/spring-boot/build.gradle .
COPY example-projects/spring-boot/gradle.properties .
COPY example-projects/spring-boot/src ./src

# Make gradlew executable
RUN chmod +x gradlew

# Build the Spring Boot application (JAR will be named project-2.0.3.jar based on directory name)
RUN ./gradlew bootJar --no-daemon -q

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage (project-2.0.3.jar based on project directory name)
COPY --from=builder /project/build/libs/project-*.jar target.jar

# Expose the default Spring Boot port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]