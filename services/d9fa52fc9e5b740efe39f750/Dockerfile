# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project for multi-module build
COPY . .

# Build the WAR with zxingorg profile (requires JDK 17+)
# This will build core, javase, and zxingorg modules
RUN mvn clean package -Pzxingorg -DskipTests -B

# Stage 2: Deploy WAR to Tomcat
FROM tomcat:10.1-jdk17

# Remove default webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy the built WAR to Tomcat webapps
# The WAR is named zxingorg-3.5.5-SNAPSHOT.war, we'll rename it to ROOT.war for root context
COPY --from=builder /app/zxingorg/target/zxingorg-3.5.5-SNAPSHOT.war /usr/local/tomcat/webapps/ROOT.war

# Create scan directory and copy WAR for security scanning
# The security scanner will access this via volume mount
RUN mkdir -p /scan /app && \
    cp /usr/local/tomcat/webapps/ROOT.war /scan/ROOT.war && \
    # Also create app.jar for security scanner
    cp /usr/local/tomcat/webapps/ROOT.war /app/target.jar && \
    chown -R 1000:1000 /scan /app

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose default Tomcat port
EXPOSE 8080

# Set environment variables
ENV JAVA_OPTS="-Djava.awt.headless=true"

# Start with entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD ["catalina.sh", "run"]