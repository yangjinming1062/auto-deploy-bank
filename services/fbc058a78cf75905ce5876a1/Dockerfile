# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set JAVA_HOME for the build
ENV JAVA_HOME=/opt/java/openjdk

WORKDIR /app

# Copy pom.xml and all module pom.xml files
COPY pom.xml /app/
COPY soap-server/pom.xml /app/soap-server/
COPY soap-common/pom.xml /app/soap-common/
COPY soap-legacy/pom.xml /app/soap-legacy/
COPY soap-builder/pom.xml /app/soap-builder/
COPY soap-client/pom.xml /app/soap-client/
COPY soap-it/pom.xml /app/soap-it/
COPY soap-test/pom.xml /app/soap-test/
COPY soap-examples /app/soap-examples/

# Copy all source directories (modules needed for soap-server)
COPY soap-server/src /app/soap-server/src
COPY soap-common/src /app/soap-common/src
COPY soap-legacy/src /app/soap-legacy/src
COPY soap-builder/src /app/soap-builder/src
COPY soap-client/src /app/soap-client/src
COPY soap-it/src /app/soap-it/src
COPY soap-test/src /app/soap-test/src

# Build the project (skip tests for speed)
RUN mvn clean package -DskipTests -B -Dmaven.javadoc.skip=true -Dlicense.skip=true -pl soap-common,soap-builder,soap-server -am

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the JAR file from builder stage
COPY --from=builder /app/soap-server/target.jar ./target.jar

# Expose the default HTTP port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]