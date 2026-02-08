# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy project structure and pom.xml
COPY pom.xml .
COPY shared/pom.xml ./shared/pom.xml
COPY util/pom.xml ./util/pom.xml
COPY stt/pom.xml ./stt/pom.xml
COPY translator/pom.xml ./translator/pom.xml
COPY nlp/pom.xml ./nlp/pom.xml
COPY bot/pom.xml ./bot/pom.xml
COPY gen-ai/pom.xml ./gen-ai/pom.xml

# Copy all module pom.xml files recursively
COPY shared/ ./shared/
COPY util/ ./util/
COPY stt/ ./stt/
COPY translator/ ./translator/
COPY nlp/ ./nlp/
COPY bot/ ./bot/
COPY gen-ai/ ./gen-ai/

# Download dependencies (go-offline)
RUN mvn dependency:go-offline -B

# Build the project (skip tests, create fat jar)
RUN mvn package -DskipTests -B -pl bot/admin/server -am

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Set working directory
WORKDIR /app

# Copy the fat jar from builder stage
COPY --from=builder /app/bot/admin/server/target/target.jar target.jar

# Expose the application port (default 8080)
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]