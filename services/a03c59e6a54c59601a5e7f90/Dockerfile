FROM python:3.11-slim

# Install system dependencies including Java JRE
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    apt-transport-https \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV BIGDL_VERSION=2.4.0
ENV SPARK_VERSION=2.4.6

# Create working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\
# Initialize Cluster Serving (download JAR if needed)\necho "Initializing Cluster Serving..."\n\
cluster-serving-init\n\
\n\
# Find the http JAR file\n\
HTTP_JAR=$(find /app -maxdepth 1 -name "*http.jar" | head -1)\n\
if [ -z "$HTTP_JAR" ]; then\n\
    echo "Error: http.jar not found"\n\
    exit 1\n\
fi\n\
\n\
# Start HTTP server using the jar with Main-Class manifest\necho "Starting HTTP server..."\n\
java -XX:+UseG1GC -Xms2g -Xmx4g -jar $HTTP_JAR\n\
' > /app/start-serving.sh && chmod +x /app/start-serving.sh

EXPOSE 10020

CMD ["/app/start-serving.sh"]