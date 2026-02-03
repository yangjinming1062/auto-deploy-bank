# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /build

# Copy entire project (Maven needs all module directories for parent POM)
COPY . /build/

# Install project to local repository and copy dependencies
RUN mvn clean install -DskipTests -B && \
    mvn dependency:copy-dependencies -DoutputDirectory=/build/deps -B

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy the main examples JAR as app.jar and target.jar for security scanning
COPY --from=builder /build/RankSys-examples/target/RankSys-examples-*.jar /app/app.jar
COPY --from=builder /build/RankSys-examples/target/RankSys-examples-*.jar /app/target.jar

# Copy all module JARs for classpath
COPY --from=builder /build/RankSys-*/target/*.jar /app/lib/

# Copy external dependencies
COPY --from=builder /build/deps/*.jar /app/ext/

# Expose default port
EXPOSE 8080

# Run the Java application with classpath
CMD ["java", "-cp", "app.jar:lib/*:ext/*", "org.ranksys.examples.WebServiceExample"]