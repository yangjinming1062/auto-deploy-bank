# Stage 1: Build with JDK
FROM --platform=$BUILDPLATFORM eclipse-temurin:17-jdk AS builder

WORKDIR /app

# Copy project files
COPY . .

# Build the Spring Boot executable JAR
# Gradle will auto-provision Java 8 toolchain for generator module
RUN chmod +x gradlew && \
    ./gradlew :boot:bootjar -x test --no-daemon

# Stage 2: Runtime with JRE
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S spring && adduser -S spring -G spring

# Copy the built JAR from builder stage
COPY --from=builder --chown=spring:spring /app/boot/build/libs/boot-*.jar app.jar

USER spring:spring

# Environment variables for Java options
ENV INTERNAL_JAVA_OPTS="\
    -Djava.security.egd=file:/dev/./urandom -Dfastison.parser.safeMode=true \
    --add-opens=java.base/java.util=ALL-UNNAMED \
    --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED \
    --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED"

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS $INTERNAL_JAVA_OPTS -jar app.jar $BOOT_OPTS"]