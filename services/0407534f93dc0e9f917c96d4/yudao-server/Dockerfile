# Runtime stage - use pre-built JAR
FROM eclipse-temurin:17-jre-alpine

# Create application directory
RUN mkdir -p /app
WORKDIR /app

# Set timezone
ENV TZ=Asia/Shanghai

# Set Java options
ENV JAVA_OPTS="-Xms512m -Xmx512m -Djava.security.egd=file:/dev/./urandom"
ENV ARGS=""

# Copy pre-built JAR
COPY yudao-server/target/yudao-server.jar app.jar

# Expose port
EXPOSE 48080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:48080/actuator/health || exit 1

# Start application
CMD java ${JAVA_OPTS} -jar app.jar $ARGS