# Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml first to leverage Docker cache for dependencies
COPY pom.xml .
COPY agileboot-admin/pom.xml agileboot-admin/
COPY agileboot-domain/pom.xml agileboot-domain/
COPY agileboot-infrastructure/pom.xml agileboot-infrastructure/
COPY agileboot-common/pom.xml agileboot-common/
COPY agileboot-api/pom.xml agileboot-api/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY . .

# Build the application
# Configure Maven to skip filtering for binary files
RUN mvn clean package -DskipTests -B \
    -Dmaven.resources.skip=true

# Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage to target directory for volume mounting
COPY --from=builder /build/agileboot-admin/target/agileboot-admin-*.jar /app/target.jar

# Expose port 8080
EXPOSE 8080

# Set JVM options for containerized environment
ENV JAVA_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"

# Run the application in foreground
CMD ["sh", "-c", "java $JAVA_OPTS -jar /app/target.jar"]