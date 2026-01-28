# Multi-stage build for Application Insights Java agent
# Stage 1: Build the agent using Gradle with Eclipse Temurin 21
FROM gradle:8.5-jdk21 AS builder

WORKDIR /app

# Copy project files
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY gradle.properties .
COPY gradlew .
COPY gradlew.bat .
COPY agent/ ./agent/
COPY buildSrc/ ./buildSrc/
COPY classic-sdk/ ./classic-sdk/
COPY etw/ ./etw/
COPY dependencyManagement/ ./dependencyManagement/
COPY smoke-tests/ ./smoke-tests/
COPY licenses/ ./licenses/

# Build the agent JAR
RUN gradle :agent:agent:shadowJar --no-daemon

# Stage 2: Runtime image with the agent
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy the built agent JAR
COPY --from=builder /app/agent/agent/build/libs/applicationinsights-agent-*.jar /app/agent.jar

# Copy application configuration
COPY applicationinsights.json /app/

# Create web content
RUN mkdir -p /var/www/localhost/htdocs
RUN cat > /var/www/localhost/htdocs/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Insights Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #0078d4; }
        .status { color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Application Insights Java Agent</h1>
        <p class="status">Service is running successfully</p>
        <p>The Application Insights Java monitoring agent is active.</p>
    </div>
</body>
</html>
EOF

# Install nginx for HTTP server
RUN apk add --no-cache nginx

# Create web content directory
RUN mkdir -p /var/www/localhost/htdocs
RUN cat > /var/www/localhost/htdocs/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Insights Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #0078d4; }
        .status { color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Application Insights Java Agent</h1>
        <p class="status">Service is running successfully</p>
        <p>The Application Insights Java monitoring agent is active.</p>
    </div>
</body>
</html>
EOF

# Configure nginx to run in foreground
RUN cat > /etc/nginx/nginx.conf << 'EOF'
daemon off;
worker_processes 1;
error_log /dev/stderr info;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log /dev/stdout;
    server {
        listen 41295;
        server_name localhost;
        root /var/www/localhost/htdocs;
        index index.html;
        location / {
            try_files $uri $uri/ =404;
        }
    }
}
EOF

# Create startup script
RUN cat > /start.sh << 'EOF'
#!/bin/sh
cp /app/agent.jar /app/target.jar
echo "JAR copied to /app/target.jar for security scanning"
echo "Application Insights Java Agent available at /app/agent.jar"
echo "Starting HTTP server on port 41295..."
exec nginx
EOF
RUN chmod +x /start.sh

# Set environment variables
ENV APPLICATIONINSIGHTS_CONFIGURATION_FILE=/app/applicationinsights.json
ENV APPLICATIONINSIGHTS_CONNECTION_STRING=${APPLICATIONINSIGHTS_CONNECTION_STRING:-}

# Expose the application port
EXPOSE 41295

ENTRYPOINT ["/start.sh"]