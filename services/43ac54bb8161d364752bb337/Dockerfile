# Stage 1: Build with Gradle
FROM gradle:8.5-jdk8 AS builder

WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle settings.gradle ./
COPY gradle ./gradle/

# Copy all subproject build files
COPY ndbench-api/build.gradle ./ndbench-api/
COPY ndbench-aws/build.gradle ./ndbench-aws/
COPY ndbench-cass-plugins/build.gradle ./ndbench-cass-plugins/
COPY ndbench-cli/build.gradle ./ndbench-cli/
COPY ndbench-core/build.gradle ./ndbench-core/
COPY ndbench-cockroachdb-plugins/build.gradle ./ndbench-cockroachdb-plugins/
COPY ndbench-dynamodb-plugins/build.gradle ./ndbench-dynamodb-plugins/
COPY ndbench-dyno-plugins/build.gradle ./ndbench-dyno-plugins/
COPY ndbench-es-plugins/build.gradle ./ndbench-es-plugins/
COPY ndbench-geode-plugins/build.gradle ./ndbench-geode-plugins/
COPY ndbench-janusgraph-plugins/build.gradle ./ndbench-janusgraph-plugins/
COPY ndbench-sample-plugins/build.gradle ./ndbench-sample-plugins/
COPY ndbench-web/build.gradle ./ndbench-web/

# Copy source files
COPY ndbench-api/src ./ndbench-api/src
COPY ndbench-aws/src ./ndbench-aws/src
COPY ndbench-cass-plugins/src ./ndbench-cass-plugins/src
COPY ndbench-cli/src ./ndbench-cli/src
COPY ndbench-core/src ./ndbench-core/src
COPY ndbench-cockroachdb-plugins/src ./ndbench-cockroachdb-plugins/src
COPY ndbench-dynamodb-plugins/src ./ndbench-dynamodb-plugins/src
COPY ndbench-dyno-plugins/src ./ndbench-dyno-plugins/src
COPY ndbench-es-plugins/src ./ndbench-es-plugins/src
COPY ndbench-geode-plugins/src ./ndbench-geode-plugins/src
COPY ndbench-janusgraph-plugins/src ./ndbench-janusgraph-plugins/src
COPY ndbench-sample-plugins/src ./ndbench-sample-plugins/src
COPY ndbench-web/src ./ndbench-web/src

# Build the WAR file (skip tests for faster build)
RUN gradle :ndbench-web:war -x test -x check --no-daemon

# Stage 2: Run with Tomcat
FROM tomcat:9.0-jdk8

# Install zip for modifying JARs
RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*

# Remove default Tomcat webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy and extract the WAR from builder stage
COPY --from=builder /build/ndbench-web/build/libs/ndbench-web.war /tmp/ROOT.war

# Remove config files from JARs inside WAR and extract
RUN mkdir -p /usr/local/tomcat/webapps/ROOT && \
    cd /usr/local/tomcat/webapps/ROOT && \
    jar xf /tmp/ROOT.war && \
    rm /tmp/ROOT.war && \
    # Remove duplicate JARs with version numbers (e.g., ndbench-core-0.7.4.jar, ndbench-api-0.7.4.jar)
    rm -f /usr/local/tomcat/webapps/ROOT/WEB-INF/lib/ndbench-[a-z]*-[0-9]*.jar && \
    # Remove application.properties from ndbench-core.jar to avoid conflicts (JAR is ZIP format)
    zip -d /usr/local/tomcat/webapps/ROOT/WEB-INF/lib/ndbench-core.jar application.properties clusters.json 2>/dev/null || true

# Copy config files to WEB-INF/classes (this file will be used by Archaius)
COPY --from=builder /build/ndbench-core/src/main/resources/application.properties /usr/local/tomcat/webapps/ROOT/WEB-INF/classes/
COPY --from=builder /build/ndbench-core/src/main/resources/clusters.json /usr/local/tomcat/webapps/ROOT/WEB-INF/classes/

# Copy WAR as target.jar for security scanning
COPY --from=builder /build/ndbench-web/build/libs/ndbench-web.war /app/target.jar

# Expose default Tomcat port
EXPOSE 8080

# Set environment variables
ENV DISCOVERY_ENV=Local

# Create setenv.sh with JVM options
RUN echo 'CATALINA_OPTS="-Dndbench.config.numKeys=10000 -Dndbench.config.writeRateLimit=35 -Dndbench.config.readRateLimit=45"' > /usr/local/tomcat/bin/setenv.sh && \
    chmod +x /usr/local/tomcat/bin/setenv.sh

# Run Tomcat in foreground
CMD ["catalina.sh", "run"]