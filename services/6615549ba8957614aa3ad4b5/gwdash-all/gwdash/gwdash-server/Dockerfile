# Multi-stage build for gwdash-server
# This Dockerfile expects a pre-built JAR at gwdash-all/gwdash/target.jar
# Build workflow:
#   1. Build Maven project (requires access to internal Xiaomi Maven repos):
#      cd /home/ubuntu/deploy-projects/6615549ba8957614aa3ad4b5/gwdash-all/gwdash && mvn clean package -DskipTests
#   2. Symlink the built JAR:
#      cd /home/ubuntu/deploy-projects/6615549ba8957614aa3ad4b5/gwdash-all/gwdash
#      ln -sf gwdash-server/target/gwdash-server-0.0.1-SNAPSHOT.jar target.jar
#   3. Build Docker image:
#      cd /home/ubuntu/deploy-projects/6615549ba8957614aa3ad4b5 && docker compose build
#   4. Start services:
#      docker compose up -d

# Stage 1: JRE layer
FROM eclipse-temurin:17-jre-alpine AS jre

# Stage 2: Runtime image
FROM alpine:3.18

# Copy JRE from builder stage
COPY --from=jre /opt/java/openjdk /opt/java

# Set JAVA_HOME
ENV JAVA_HOME=/opt/java
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app

# Create log directory and user
RUN mkdir -p /app/log && \
    adduser -D -u 1000 app && \
    chown -R app:app /app

# Copy the pre-built JAR from the Maven build context
# The build context is /home/ubuntu/deploy-projects/6615549ba8957614aa3ad4b5
# gwdash-all/gwdash/target.jar should be a symlink to the actual built JAR
COPY --chown=app:app gwdash-all/gwdash/target.jar app.jar

# Switch to non-root user
USER app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]