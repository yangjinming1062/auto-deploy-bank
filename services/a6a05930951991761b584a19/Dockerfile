# Runtime image with JRE
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Install required tools
RUN apk add --no-cache curl bash && rm -rf /var/cache/apk/*

# Create startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'while [ ! -f /app/target.jar ]; do' >> /app/start.sh && \
    echo '    echo "Waiting for target.jar to be mounted..."' >> /app/start.sh && \
    echo '    sleep 1' >> /app/start.sh && \
    echo 'done' >> /app/start.sh && \
    echo 'echo "Starting Cloudbreak..."' >> /app/start.sh && \
    echo 'exec java -jar /app/target.jar' >> /app/start.sh && \
    chmod +x /app/start.sh

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

# Expose the main service port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/cb/actuator/health || exit 1

# Run the application via startup script
ENTRYPOINT ["/app/start.sh"]