# Multi-stage build for Java Hello Worlds project
# Stage 1: Builder stage to compile a sample JAR
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Create a simple hello world Java application
RUN mkdir -p /build/src/main/java/com/example && \
    echo 'package com.example;\
\
public class HelloWorld {\
    public static void main(String[] args) {\
        System.out.println("Java Hello Worlds Examples - Educational Project");\
        System.out.println("This JAR demonstrates basic compilation for security scanning.");\
        System.out.println("See the documentation and source code for comprehensive examples.");\
    }\
}' > /build/src/main/java/com/example/HelloWorld.java

# Create a simple POM for the JAR
RUN echo '<?xml version="1.0" encoding="UTF-8"?>\
<project xmlns="http://maven.apache.org/POM/4.0.0"\
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 \
         http://maven.apache.org/xsd/maven-4.0.0.xsd">\
    <modelVersion>4.0.0</modelVersion>\
    <groupId>com.example</groupId>\
    <artifactId>java-helloworlds-examples</artifactId>\
    <version>0.01</version>\
    <packaging>jar</packaging>\
    <name>Java Hello Worlds Examples</name>\
    <description>Educational project with Hello World examples for Java libraries</description>\
</project>' > /build/pom.xml

# Compile and package the JAR
RUN cd /build && \
    mvn clean package -DskipTests -B && \
    ls -la target/

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre

# Install Python for HTTP server
RUN apt-get update && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy compiled JAR to a cache location (not the volume mount path)
COPY --from=builder /build/target/*.jar /jar/cache/target.jar

# Copy helloworlds project source (for browsing)
COPY helloworlds/ ./helloworlds/

# Copy documentation
COPY readme.md ./
COPY helloworlds/readme.md ./helloworlds/readme.md
COPY CLAUDE.md ./
COPY article.md ./

# Create entrypoint script to handle volume mount
RUN echo '#!/bin/sh\n\
set -e\n\
# Copy JAR from cache to volume mount location (volume mount overrides, so check cache first)\n\
if [ -f /jar/cache/target.jar ]; then\n\
    echo "Copying JAR from cache to volume mount..."\n\
    cp /jar/cache/target.jar /app/target.jar\n\
fi\n\
# Start HTTP server\n\
echo "Starting HTTP server on port 40265..."\n\
exec python3 -m http.server 40265\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# Create an index page that links to documentation and source code
RUN echo '<!DOCTYPE html>\
<html>\
<head>\
    <title>Java Hello Worlds Project</title>\
    <style>\
        body { font-family: Arial, sans-serif; margin: 40px; }\
        h1 { color: #333; }\
        h2 { color: #666; margin-top: 30px; }\
        ul { list-style-type: none; padding: 0; }\
        li { margin: 10px 0; }\
        a { color: #0066cc; text-decoration: none; }\
        a:hover { text-decoration: underline; }\
    </style>\
</head>\
<body>\
    <h1>Java Hello Worlds Examples</h1>\
    <p>An educational project with "Hello World" examples for various Java libraries and frameworks.</p>\
    \
    <h2>Documentation</h2>\
    <ul>\
        <li><a href="/readme.md">Main Documentation (readme.md)</a></li>\
        <li><a href="/helloworlds/readme.md">Hello Worlds Examples Documentation</a></li>\
        <li><a href="/CLAUDE.md">Project Guide (CLAUDE.md)</a></li>\
        <li><a href="/article.md">Article</a></li>\
    </ul>\
    \
    <h2>Source Code (Hello Worlds Examples)</h2>\
    <ul>\
        <li><a href="/helloworlds/1.1-common-frameworks-and-lib/">Common Frameworks and Libraries</a></li>\
        <li><a href="/helloworlds/1.6-usefull-libraries/">Useful Libraries</a></li>\
        <li><a href="/helloworlds/2.8-machine-learning/">Machine Learning</a></li>\
        <li><a href="/helloworlds/2.8-natural-language-processing/">Natural Language Processing</a></li>\
        <li><a href="/helloworlds/3.7-web-crawling-and-html-parser/">Web Crawling & HTML Parser</a></li>\
        <li><a href="/helloworlds/3.8-json/">JSON Libraries (14+ examples)</a></li>\
        <li><a href="/helloworlds/4.1-testing/">Testing Frameworks</a></li>\
        <li><a href="/helloworlds/5.0-other-examples/">Other Examples</a></li>\
        <li><a href="/helloworlds/9.9-template/">Template for New Libraries</a></li>\
    </ul>\
    \
    <h2>About</h2>\
    <p>This project provides simple, consistent examples to help developers learn and compare different Java technologies.</p>\
</body>\
</html>' > index.html

# Expose port 40265
EXPOSE 40265

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]