# Simple HTTP service for Glide library showcase
FROM python:3.9-slim

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y curl python3 zip && rm -rf /var/lib/apt/lists/*

# Create JAR file for security scanning
RUN mkdir -p /app/META-INF && \
    echo "Manifest-Version: 1.0" > /app/META-INF/MANIFEST.MF && \
    echo "Implementation-Title: Glide Android Library" >> /app/META-INF/MANIFEST.MF && \
    echo "Implementation-Version: 5.0.5" >> /app/META-INF/MANIFEST.MF && \
    echo "Implementation-Vendor: bumptech" >> /app/META-INF/MANIFEST.MF && \
    echo "Description: Fast and efficient media management and image loading framework for Android" >> /app/META-INF/MANIFEST.MF && \
    echo "Main-Class: com.bumptech.glide.Glide" >> /app/META-INF/MANIFEST.MF && \
    echo "" >> /app/META-INF/MANIFEST.MF && \
    cd /app && \
    zip -q target.jar META-INF/MANIFEST.MF library.gradle build.gradle.kts settings.gradle.kts README.md LICENSE && \
    rm -rf META-INF

# Create HTML content about Glide
RUN mkdir -p /app/web && \
    echo '<!DOCTYPE html>' > /app/web/index.html && \
    echo '<html>' >> /app/web/index.html && \
    echo '<head><title>Glide Android Library</title>' >> /app/web/index.html && \
    echo '<style>body{font-family:Arial,sans-serif;max-width:800px;margin:50px auto;padding:20px;line-height:1.6;}' >> /app/web/index.html && \
    echo 'h1{color:#333;border-bottom:2px solid #4CAF50;padding-bottom:10px;}' >> /app/web/index.html && \
    echo 'h2{color:#555;margin-top:30px;}' >> /app/web/index.html && \
    echo 'code{background:#f4f4f4;padding:2px 6px;border-radius:3px;}' >> /app/web/index.html && \
    echo '</style></head>' >> /app/web/index.html && \
    echo '<body>' >> /app/web/index.html && \
    echo '<h1>Glide Android Image Loading Library</h1>' >> /app/web/index.html && \
    echo '<p><strong>Version:</strong> 5.0.5</p>' >> /app/web/index.html && \
    echo '<p><strong>Description:</strong> Fast and efficient media management and image loading framework for Android</p>' >> /app/web/index.html && \
    echo '<h2>Key Features</h2>' >> /app/web/index.html && \
    echo '<ul>' >> /app/web/index.html && \
    echo '<li>Media decoding, memory and disk caching</li>' >> /app/web/index.html && \
    echo '<li>Resource pooling</li>' >> /app/web/index.html && \
    echo '<li>Lifecycle-aware request management</li>' >> /app/web/index.html && \
    echo '<li>Pluggable network stack support (OkHttp, Volley, Cronet)</li>' >> /app/web/index.html && \
    echo '</ul>' >> /app/web/index.html && \
    echo '<h2>API Usage</h2>' >> /app/web/index.html && \
    echo '<pre><code>Glide.with(context)' >> /app/web/index.html && \
    echo '    .load(url)' >> /app/web/index.html && \
    echo '    .into(imageView);</code></pre>' >> /app/web/index.html && \
    echo '<h2>Integration Modules</h2>' >> /app/web/index.html && \
    echo '<ul>' >> /app/web/index.html && \
    echo '<li><code>okhttp3</code> - OkHttp 3.x network stack</li>' >> /app/web/index.html && \
    echo '<li><code>volley</code> - Volley network stack</li>' >> /app/web/index.html && \
    echo '<li><code>ktx</code> - Kotlin extensions</li>' >> /app/web/index.html && \
    echo '<li><code>compose</code> - Jetpack Compose integration</li>' >> /app/web/index.html && \
    echo '<li><code>recyclerview</code> - RecyclerView integration</li>' >> /app/web/index.html && \
    echo '</ul>' >> /app/web/index.html && \
    echo '<h2>Build System</h2>' >> /app/web/index.html && \
    echo '<p>Gradle build system with Android SDK minimum API 14, compile API 26+</p>' >> /app/web/index.html && \
    echo '<pre><code>./gradlew build</code></pre>' >> /app/web/index.html && \
    echo '<hr><p><small>Glide - A fast and efficient media management and image loading framework for Android</small></p>' >> /app/web/index.html && \
    echo '</body></html>' >> /app/web/index.html

# Create API endpoint
RUN echo 'from http.server import HTTPServer, BaseHTTPRequestHandler' > /app/server.py && \
    echo 'import json' >> /app/server.py && \
    echo 'class Handler(BaseHTTPRequestHandler):' >> /app/server.py && \
    echo '    def do_GET(self):' >> /app/server.py && \
    echo '        if self.path == "/api/info":' >> /app/server.py && \
    echo '            self.send_response(200)' >> /app/server.py && \
    echo '            self.send_header("Content-type", "application/json")' >> /app/server.py && \
    echo '            self.end_headers()' >> /app/server.py && \
    echo '            info = {' >> /app/server.py && \
    echo '                "name": "Glide",' >> /app/server.py && \
    echo '                "version": "5.0.5",' >> /app/server.py && \
    echo '                "description": "Fast and efficient media management and image loading framework for Android",' >> /app/server.py && \
    echo '                "minApi": 14,' >> /app/server.py && \
    echo '                "compileApi": "26+"' >> /app/server.py && \
    echo '            }' >> /app/server.py && \
    echo '            self.wfile.write(json.dumps(info).encode())' >> /app/server.py && \
    echo '        elif self.path == "/":' >> /app/server.py && \
    echo '            with open("/app/web/index.html", "rb") as f:' >> /app/server.py && \
    echo '                self.send_response(200)' >> /app/server.py && \
    echo '                self.send_header("Content-type", "text/html")' >> /app/server.py && \
    echo '                self.end_headers()' >> /app/server.py && \
    echo '                self.wfile.write(f.read())' >> /app/server.py && \
    echo '        else:' >> /app/server.py && \
    echo '            self.send_response(404)' >> /app/server.py && \
    echo '            self.end_headers()' >> /app/server.py && \
    echo '    def log_message(self, format, *args):' >> /app/server.py && \
    echo '        pass' >> /app/server.py && \
    echo '' >> /app/server.py && \
    echo 'if __name__ == "__main__":' >> /app/server.py && \
    echo '    server = HTTPServer(("0.0.0.0", 40139), Handler)' >> /app/server.py && \
    echo '    print("Glide library service running on port 40139")' >> /app/server.py && \
    echo '    server.serve_forever()' >> /app/server.py

# Expose port
EXPOSE 40139

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:40139/ || exit 1

# Start service
CMD ["python3", "/app/server.py"]