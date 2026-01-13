# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for better caching
COPY pom.xml .
COPY bizlog-sdk/pom.xml bizlog-sdk/
COPY bizlog-server/pom.xml bizlog-server/
COPY bizlog-sdk-xml/pom.xml bizlog-sdk-xml/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY bizlog-sdk/src bizlog-sdk/src
COPY bizlog-server/src bizlog-server/src
COPY bizlog-sdk-xml/src bizlog-sdk-xml/src

# Build the application
ENV MAVEN_OPTS="--add-opens=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.jvm=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED"
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy the JAR from builder stage
COPY --from=builder /app/bizlog-server/target/bizlog-server-*.jar app.jar

# Copy and set up entrypoint script
COPY extract-jar.sh /usr/local/bin/extract-jar.sh
RUN chmod +x /usr/local/bin/extract-jar.sh

# Expose port
EXPOSE 8080

# Run the application with entrypoint
ENTRYPOINT ["/usr/local/bin/extract-jar.sh"]
CMD ["java", "-jar", "app.jar"]