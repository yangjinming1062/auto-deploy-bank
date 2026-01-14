# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Set Maven memory options for builds
ENV MAVEN_OPTS="-Xms4g -Xmx4g"

# Copy Maven settings to allow HTTP repository access
COPY settings.xml /usr/share/maven/conf/settings.xml

# Use patched pom.xml that removes unreachable repository and ansj dependency
COPY pom.xml.docker pom.xml

# Copy source code, lib, and data folders
COPY src ./src
COPY lib ./lib
COPY data ./data

# Remove AnsjEvaluation.java since ansj dependency is unavailable
RUN rm -f /app/src/org/apdplat/evaluation/impl/AnsjEvaluation.java

# Remove Ansj references from WordSegmenter.java
RUN sed -i '/Ansj分词器/d' /app/src/org/apdplat/evaluation/WordSegmenter.java

# Build the fat JAR with all dependencies
RUN mvn clean package -DskipTests -B -s /usr/share/maven/conf/settings.xml

# Add Main-Class to manifest for web server
RUN cd /app/target && \
    mkdir -p META-INF && \
    echo "Manifest-Version: 1.0" > META-INF/MANIFEST.MF && \
    echo "Main-Class: org.apdplat.evaluation.web.WebServer" >> META-INF/MANIFEST.MF && \
    jar xf cws_evaluation-1.1.jar org && \
    jar xf cws_evaluation-1.1.jar com && \
    jar cfm cws_evaluation-1.1.jar META-INF/MANIFEST.MF org com && \
    mv cws_evaluation-1.1.jar app.jar && \
    rm -rf META-INF org com

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the fat JAR from builder stage (renamed to app.jar in builder stage)
COPY --from=builder /app/target/app.jar app.jar

# Copy data folder for test evaluation
COPY --from=builder /app/data ./data

# Copy lib folder for FudanNLP and Jcseg resources
COPY --from=builder /app/lib ./lib

# Create entrypoint script to copy JAR for security scanning
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
# Create target.jar for security scanning (overwrites mounted file)
cp /app/app.jar /app/target.jar
# Run the web server with increased heap for memory-intensive NLP processing
exec java -Xmx3g -jar /app/app.jar
EOF

ENTRYPOINT ["/entrypoint.sh"]
CMD []
