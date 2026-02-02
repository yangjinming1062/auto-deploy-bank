# Stage 1: Build stage using Maven and Eclipse Temurin 17
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the project (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage using Eclipse Temurin 17 JRE Alpine
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built WAR (Spring Boot executable WAR) from builder stage
# The WAR file is renamed to app.jar for security scanning consistency
COPY --from=builder /app/target/*.war app.jar

# Extract JSP files for proper rendering (Spring Boot WAR has JSP limitations)
RUN unzip -q app.jar -d /app/war && \
    mkdir -p /app/classes/WEB-INF/jsp && \
    cp -r /app/war/WEB-INF/jsp/* /app/classes/WEB-INF/jsp/ && \
    rm -rf /app/war

# Create application.properties with JSP view resolver configuration
RUN mkdir -p /app/classes && \
    echo 'spring.mvc.view.prefix=/WEB-INF/jsp/' > /app/classes/application.properties && \
    echo 'spring.mvc.view.suffix=.jsp' >> /app/classes/application.properties && \
    echo 'server.address=0.0.0.0' >> /app/classes/application.properties

# Expose the application port (configured as 9090 in application.properties)
EXPOSE 9090

# Run the application (Spring Boot WAR files are executable)
# Force IPv4 to ensure external accessibility
CMD ["java", "-Djava.net.preferIPv4Stack=true", "-jar", "app.jar"]