# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the JAR (skip tests since this is a library and tests require a database)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/pgjdbc-ng-0.0.1-SNAPSHOT.jar app.jar

# Expose port 8080
EXPOSE 8080

# Run the JAR
CMD ["java", "-jar", "app.jar"]