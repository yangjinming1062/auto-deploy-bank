# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Copy codingstyle directory for checkstyle
COPY codingstyle ./codingstyle

# Build the project
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/Soot-4.0-SNAPSHOT.jar target.jar

EXPOSE 40932

CMD ["java", "-jar", "target.jar"]