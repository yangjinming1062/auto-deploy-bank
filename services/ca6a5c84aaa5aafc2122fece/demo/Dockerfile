# Stage 1: Build
FROM docker.io/maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy the entire parent project first
COPY . .

# Install all parent modules (builds langchain4j-spring-boot-starter and other dependencies)
RUN mvn clean install -DskipTests -B -pl langchain4j-spring-boot-starter

# Build the demo application
RUN mvn clean package -DskipTests -B -f demo/pom.xml

# Stage 2: Runtime
FROM docker.io/eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/demo/target/*.jar app.jar

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]