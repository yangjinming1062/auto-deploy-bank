# Multi-stage Dockerfile for RackShift multi-module project
# This builds the frontend, copies it to backend static resources, and builds the backend

# Stage 1: Build frontend
FROM node:20 AS frontend-builder

WORKDIR /app

# Copy frontend package files
COPY rackshift-web/package*.json ./
RUN npm install

# Copy frontend source and build
COPY rackshift-web/ ./
RUN npm run build

# Stage 2: Build backend with frontend integrated
FROM maven:3-eclipse-temurin-17 AS backend-builder

WORKDIR /app

# Copy frontend build output to a temporary location
COPY --from=frontend-builder /app/dist /tmp/frontend-dist

# Copy parent pom.xml (modified to exclude problematic modules)
COPY pom.xml .

# Create modified parent pom.xml without rackshift-web, rackshift-proxy, rackshift-dhcp-proxy modules
RUN sed -i -e '/<module>rackshift-web<\/module>/d' \
           -e '/<module>rackshift-proxy<\/module>/d' \
           -e '/<module>rackshift-dhcp-proxy<\/module>/d' pom.xml

# Copy rackshift-plugin with all sub-modules
COPY rackshift-plugin/ ./rackshift-plugin/

# Copy rackshift-server
COPY rackshift-server/ ./rackshift-server/

# Step 1: Install all plugin modules to local Maven repository in order
WORKDIR /app
RUN cd rackshift-plugin/metal-plugin-sdk && \
    mvn install -DskipTests -Dmaven.javadoc.skip=true -B && \
    cd ../dell-metal-plugin && \
    mvn install -DskipTests -Dmaven.javadoc.skip=true -B && \
    cd ../inspur-metal-plugin && \
    mvn install -DskipTests -Dmaven.javadoc.skip=true -B && \
    cd ../hp-metal-plugin && \
    mvn install -DskipTests -Dmaven.javadoc.skip=true -B && \
    cd ../h3c-metal-plugin && \
    mvn install -DskipTests -Dmaven.javadoc.skip=true -B && \
    cd ../inspurm5-metal-plugin && \
    mvn install -DskipTests -Dmaven.javadoc.skip=true -B && \
    cd ../..

# Step 2: Build rackshift-server with frontend static resources
WORKDIR /app/rackshift-server
RUN mkdir -p src/main/resources/static && \
    cp -r /tmp/frontend-dist/* src/main/resources/static/ && \
    mvn clean package -DskipTests -B

# Stage 3: Runtime image
FROM eclipse-temurin:17-jre

WORKDIR /app

# Install curl and lsof for health checks and port checking
RUN apt-get update && apt-get install -y curl lsof && rm -rf /var/lib/apt/lists/*

# Create target directory for volume mount
RUN mkdir -p /app/target

# Copy JAR from builder stage
COPY --from=backend-builder /app/rackshift-server/target/rackshift-server-1.0.0.jar app.jar

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy JAR to target directory for volume mounting and security scanning
RUN cp /app/app.jar /app/target.jar

# Create directories for application data
RUN mkdir -p /opt/rackshift/logs/rackshift /opt/rackshift/conf

# Expose port
EXPOSE 8082

# Start application via entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
