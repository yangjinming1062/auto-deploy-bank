# Multi-stage build for t-digest web service
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /build

# Copy pom.xml and source code for t-digest library
COPY core ./core
COPY pom.xml .

# Build the t-digest library first
RUN mvn clean install -DskipTests -B

# Now set up the service application
COPY service-pom.xml pom.xml
RUN mkdir -p src/main/java/com/tdunning
COPY ServiceApp.java src/main/java/com/tdunning/
RUN touch src/main/java/com/tdunning/ServiceApp.java

# Copy the built t-digest JAR to where the service expects it
RUN mkdir -p core/target
RUN cp /root/.m2/repository/com/tdunning/t-digest/3.4-SNAPSHOT/t-digest-3.4-SNAPSHOT.jar core/target/

# Build the service application
RUN mvn clean package -DskipTests -B

# Runtime stage
FROM eclipse-temurin:17-jre

# Set working directory
WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /build/target/t-digest-service-1.0.0.jar app.jar

# Expose port 8080
EXPOSE 8080

# Create a marker file to indicate the service is ready
RUN echo "t-digest web service is ready" > /app/service-ready.txt

# Run the Spring Boot application
CMD ["java", "-jar", "app.jar"]