# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 as builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src

# Build with Java 17 compatibility flags for Lombok
ENV MAVEN_OPTS="--add-opens jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.jvm=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED --add-opens jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED"
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy the built jar from builder stage
COPY --from=builder /app/target/warehouse-0.0.1-SNAPSHOT.jar app.jar

# For security scanning: copy to the volume mount path
# When running with docker compose, host's ./target.jar will be mounted to /target.jar
# The security scanner can scan either /app.jar (inside container) or ./target.jar (on host)

# Expose the application port
EXPOSE 8888

# Run the application
CMD ["java", "-jar", "app.jar"]