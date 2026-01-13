# Multi-stage build for JAR application
# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# First build the parent project to get all dependencies
COPY pom.xml .
COPY modules ./modules

# Install parent POM first
RUN mvn install -DskipTests -N

# Install all the Swagger Core modules at once
RUN mvn install -DskipTests -pl modules/swagger-annotations,modules/swagger-models,modules/swagger-core,modules/swagger-integration,modules/swagger-jaxrs2,modules/swagger-jaxrs2-servlet-initializer -am

# Now build the sample application
WORKDIR /build/app
COPY app/pom.xml .
COPY app/src ./src

# Build the sample application as a JAR
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy the JAR file
COPY --from=builder /build/app/target/app.jar app.jar

# Copy JAR to expected location for volume mount (security scanning)
RUN mkdir -p /app/target && cp app.jar /app/target/target.jar

# Set environment variables
ENV JAVA_OPTS="-Xms512m -Xmx1024m"

# Expose port 8080
EXPOSE 8080

# Start the application
CMD ["java", "-jar", "app.jar"]
