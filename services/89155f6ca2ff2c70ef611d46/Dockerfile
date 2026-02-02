# Stage 1: Build WAR with Maven
FROM maven:3-eclipse-temurin-8 AS builder

WORKDIR /build

# Copy entire project for multi-module build
COPY . .

# Build the admin WAR (with dependencies)
RUN mvn clean package -DskipTests -B -pl admin -am

# Stage 2: Runtime with Tomcat
FROM tomcat:8.5-jre8-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Remove default Tomcat webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy the built WAR from builder stage to Tomcat webapps
COPY --from=builder /build/admin/target/ROOT.war /usr/local/tomcat/webapps/ROOT.war

# Copy WAR to /app/target.jar for security scanning
COPY --from=builder /build/admin/target/ROOT.war /app/target.jar

# Set JAVA_OPTS for memory settings
ENV JAVA_OPTS="-Xms512m -Xmx1024m"

# Expose port 8080 (Tomcat default)
EXPOSE 8080

# Run Tomcat in foreground
CMD ["catalina.sh", "run"]