# Stage 1: Build the application with Java 8
FROM maven:3.8-openjdk-8 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Create the final image with Java 8
FROM eclipse-temurin:8-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.war /app/target.jar
EXPOSE 8080
CMD ["java", "-jar", "/app/target.jar"]
