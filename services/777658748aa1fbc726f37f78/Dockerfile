# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

# Install required tools for build
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/777658748aa1fbc726f37f78

# Copy the entire project
COPY . ./

# Step 1: Install root parent POM
RUN mvn install -N -B -Dmaven.test.skip=true -Dmaven.buildNumber.skip=true -Dmdep.analyze.skip=true

# Step 2: Build and install inception-inception-dependencies (BOM for dependencies)
# This is needed by inception-app which imports it in dependencyManagement
RUN mvn install -f inception/inception-dependencies/pom.xml -B -Dmaven.test.skip=true -Dmaven.buildNumber.skip=true -Dmdep.analyze.skip=true

# Step 3: Build and install inception-test-dependencies (BOM for test dependencies)
RUN mvn install -f inception/inception-test-dependencies/pom.xml -B -Dmaven.test.skip=true -Dmaven.buildNumber.skip=true -Dmdep.analyze.skip=true

# Step 4: Build and install inception-bom (parent BOM)
RUN mvn install -f inception/inception-bom/pom.xml -B -Dmaven.test.skip=true -Dmaven.buildNumber.skip=true -Dmdep.analyze.skip=true

# Step 5: Build and install inception-app (parent pom for all app modules)
RUN mvn install -f inception/pom.xml -B -Dmaven.test.skip=true -Dmaven.buildNumber.skip=true -Dmdep.analyze.skip=true

# Step 6: Build the main webapp with standalone JAR
RUN mvn package -Pnon-m2e -B -Dmaven.test.skip=true -DskipTests -Dmaven.buildNumber.skip=true -Dmdep.analyze.skip=true -f inception/inception-app-webapp/pom.xml

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

LABEL maintainer="INCEpTION Team"

# Define network ports
EXPOSE 8080

# User and group IDs
ENV APP_USER=inception
ENV APP_UID=2000
ENV APP_GROUP=inception
ENV APP_GID=2000

# Language settings
ENV LANG=en_US.UTF-8

# Application settings
ENV JAVA_OPTS=
ENV JAVA_MEM_OPTS=-XX:MaxRAMPercentage=80

# Install application JAR
WORKDIR /opt/inception

# Copy the built JAR and rename to target.jar for security scanning
COPY --from=builder /home/ubuntu/deploy-projects/777658748aa1fbc726f37f78/inception/inception-app-webapp/target/inception-app-webapp-*-standalone.jar target.jar

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set up user and permissions with custom home directory
RUN addgroup -g ${APP_GID} ${APP_GROUP} && \
    adduser -D -H -u ${APP_UID} -G ${APP_GROUP} -s /bin/sh -h /opt/inception ${APP_USER} && \
    chown -R ${APP_USER}:${APP_GROUP} /opt/inception

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -sf http://localhost:8080/actuator/health || exit 1

# Launch application
ENTRYPOINT ["/entrypoint.sh"]