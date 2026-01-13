# Multi-stage build for Spring MVC application
# Stage 1: Build the WAR file using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml first for better caching
COPY pom.xml .

# Copy source code
COPY src ./src

# Build the WAR file
RUN mvn clean package -DskipTests -B

# Stage 2: Deploy WAR to Tomcat
FROM tomcat:8.5-alpine

# Remove default ROOT application
RUN rm -rf /usr/local/tomcat/webapps/ROOT

# Copy the built WAR to Tomcat webapps as ROOT
COPY --from=builder /build/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war

# Copy WAR as JAR for security scanning (extract to /app directory)
RUN mkdir -p /app && cp /usr/local/tomcat/webapps/ROOT.war /app/target.jar

# Copy custom server configuration if needed
# COPY server.xml /usr/local/tomcat/conf/server.xml

EXPOSE 8080

# Start Tomcat in foreground mode
CMD ["catalina.sh", "run"]