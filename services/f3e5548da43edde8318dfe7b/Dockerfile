# Multi-stage Docker build for WxJava SDK and Demo Application
# Stage 1: Build the WxJava SDK modules
FROM maven:3.9-eclipse-temurin-17 AS sdk-builder

WORKDIR /build

# Copy the root POM
COPY pom.xml .

# Copy all module POMs
COPY weixin-graal/pom.xml ./weixin-graal/
COPY weixin-java-common/pom.xml ./weixin-java-common/
COPY weixin-java-mp/pom.xml ./weixin-java-mp/
COPY weixin-java-pay/pom.xml ./weixin-java-pay/
COPY weixin-java-miniapp/pom.xml ./weixin-java-miniapp/
COPY weixin-java-cp/pom.xml ./weixin-java-cp/
COPY weixin-java-open/pom.xml ./weixin-java-open/
COPY weixin-java-channel/pom.xml ./weixin-java-channel/
COPY weixin-java-qidian/pom.xml ./weixin-java-qidian/

# Download dependencies for all modules
RUN mvn dependency:go-offline -B

# Install all SDK modules to local repository
RUN mvn clean install -DskipTests -B

# Stage 2: Build the demo application
FROM maven:3.9-eclipse-temurin-17 AS demo-builder

WORKDIR /build

# Copy demo-app files
COPY demo-app/pom.xml ./demo-app/
COPY demo-app/src ./demo-app/src

# Build the demo application using the installed SDK modules
WORKDIR /build/demo-app
RUN mvn clean package -DskipTests -B

# Stage 3: Create final runtime image
FROM maven:3.9-eclipse-temurin-17

WORKDIR /app

# Copy the built JAR from demo-builder
COPY --from=demo-builder /build/demo-app/target/wx-java-demo-*.jar app.jar

# Create a volume for security scanning
VOLUME ["/app/target.jar"]

# Expose port
EXPOSE 40358

# Health check (using curl)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:40358/api/demo/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]