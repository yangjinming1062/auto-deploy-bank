# Runtime image for JetBrains Compose Desktop application
FROM eclipse-temurin:17

# Install runtime dependencies including Xvfb and VLC for headless mode
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    xauth \
    vlc \
    libvlc-dev \
    libxi6 \
    libxtst6 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxcursor1 \
    libxrender1 \
    libxext6 \
    libxinerama1 \
    libxrandr2 \
    libglib2.0-0 \
    libglib2.0-bin \
    libcairo2 \
    libpango-1.0-0 \
    libpng16-16 \
    fonts-dejavu-core \
    libfontconfig1 \
    libfreetype6 \
    curl \
    nginx \
    && rm -rf /var/lib/apt-lists/*

WORKDIR /app

# Copy the pre-built runnable fat JAR
COPY target.jar app.jar

# Create startup script
COPY <<'EOF' /start.sh
#!/bin/bash
set -e

mkdir -p /app/logs
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

# Create nginx configuration for web access on port 40440
cat > /etc/nginx/sites-available/mujing << 'NGINX'
server {
    listen 40440;
    server_name localhost;

    location / {
        root /var/www/html;
        index index.html;
    }

    location /health {
        return 200 '{"status":"UP","service":"MuJing Compose Desktop"}';
        add_header Content-Type application/json;
    }

    location /api/status {
        return 200 '{"running":true,"type":"compose-desktop","port":40440}';
        add_header Content-Type application/json;
    }
}
NGINX
ln -sf /etc/nginx/sites-available/mujing /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Create a simple HTML page
mkdir -p /var/www/html
cat > /var/www/html/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <title>MuJing Compose Desktop</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .status { color: green; font-size: 24px; }
        .info { margin-top: 20px; color: #666; }
    </style>
</head>
<body>
    <h1>MuJing Compose Desktop Service</h1>
    <p class="status">Service Status: Running</p>
    <div class="info">
        <p>This is a JetBrains Compose Desktop application running in headless mode.</p>
        <p>Web server port: 40440</p>
        <p><a href="/health">Health Check</a> | <a href="/api/status">API Status</a></p>
    </div>
</body>
</html>
HTML

# Set up Xvfb for headless mode
export DISPLAY=:99
# Clean up any stale Xvfb lock files
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99
Xvfb :99 -screen 0 1024x768x24 &
XVFB_PID=$!

# Set VLC library path
VLC_LIB=$(find /usr -name "libvlc.so" 2>/dev/null | xargs dirname)
if [ -n "$VLC_LIB" ]; then
    export LD_LIBRARY_PATH="$VLC_LIB:$LD_LIBRARY_PATH"
fi

sleep 2

echo "Starting MuJing application and web server..."

# Start nginx
nginx &
NGINX_PID=$!

# Run the Java application in background
java \
    -Dfile.encoding=UTF-8 \
    -server \
    -Xms64m \
    -Xmx1g \
    -XX:+UseZGC \
    -jar app.jar >> /app/logs/app.log 2>&1 &
JAVA_PID=$!

# Wait for either process
wait $JAVA_PID || true

# Cleanup
kill $XVFB_PID 2>/dev/null || true
kill $NGINX_PID 2>/dev/null || true
EOF
RUN chmod +x /start.sh

VOLUME /app
EXPOSE 40440
CMD ["/start.sh"]