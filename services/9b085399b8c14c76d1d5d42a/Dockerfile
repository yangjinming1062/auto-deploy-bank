# SonarQube Docker Image - Community Edition
FROM eclipse-temurin:17-jre-alpine

WORKDIR /opt/sonarqube

# Install curl, wget, and su-exec
RUN apk add --no-cache curl wget su-exec

# Create sonarqube user and group
RUN addgroup -S sonarqube && \
    adduser -S -G sonarqube sonarqube

# Download SonarQube Community Edition 10.6
RUN wget -q -O sonarqube.zip https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-10.6.0.92116.zip

# Extract the distribution
RUN unzip -q sonarqube.zip && \
    mv sonarqube-*/* . && \
    rm -rf sonarqube-* sonarqube.zip

# Create directories and set ownership
RUN mkdir -p data extensions logs temp && \
    chown -R sonarqube:sonarqube data extensions logs temp && \
    chmod -R 755 data extensions logs temp && \
    touch logs/es.log logs/sonar.log logs/access.log logs/deploy.log logs/ce.log && \
    chown sonarqube:sonarqube logs/*.log && \
    chmod 644 logs/*.log

# Copy the main JAR for security scanning and set ownership
RUN find lib -name "sonar-application-*.jar" -exec cp {} /opt/sonarqube/target.jar \; && \
    chown sonarqube:sonarqube target.jar && \
    chmod 644 target.jar

# Set ownership for entire /opt/sonarqube
RUN chown -R sonarqube:sonarqube /opt/sonarqube

# Copy and set permissions for entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the web server port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:9000/api/system/health || exit 1

# Use entrypoint script to fix permissions then start SonarQube
ENTRYPOINT ["/entrypoint.sh"]
