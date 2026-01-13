# Multi-stage build for Apache Ignite
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy Maven configuration files and source code
COPY pom.xml .
COPY .mvn .mvn
COPY parent parent
COPY . .

# Build Apache Ignite core and dependencies (exclude numa-allocator which requires cmake)
# Build core module and everything it depends on
RUN mvn clean install -pl modules/core -am -Pall-java,licenses -DskipTests -B
# Build indexing module
RUN mvn clean install -pl modules/indexing -am -Pall-java,licenses -DskipTests -B
# Build rest-http module
RUN mvn clean install -pl modules/rest-http -am -Pall-java,licenses -DskipTests -B
# Build spring module
RUN mvn clean install -pl modules/spring -am -Pall-java,licenses -DskipTests -B
# Build binary modules
RUN mvn clean install -pl modules/binary/api,modules/binary/impl -am -Pall-java,licenses -DskipTests -B
# Copy Maven dependencies to build/libs directory
# Copy dependencies for all built modules
RUN mkdir -p /build/libs /app && \
    for module in core indexing rest-http spring; do \
        mvn dependency:copy-dependencies -DoutputDirectory=/build/libs -DincludeScope=compile -pl modules/$module -am -q || true; \
    done && \
    # Create a fat JAR for security scanning using the main Ignite core JAR
    cd /build/modules/core/target && \
    jar -xf ignite-core-2.18.0-SNAPSHOT.jar && \
    cd - && \
    # Copy Ignite classes and dependencies to /app
    (cd /build/modules/core/target/classes && jar -cf /app/target.jar .) && \
    # Add dependencies to the JAR
    for jar in /build/libs/*.jar; do \
        jar -uf /app/target.jar -C "${jar%/*}" "$(basename "$jar")" 2>/dev/null || true; \
    done

# Stage 2: Runtime image
FROM eclipse-temurin:17-jdk-alpine

# Install bash for ignite.sh script
RUN apk add --no-cache bash

# Set working directory
WORKDIR /opt/ignite

# Copy built artifacts from builder stage
# Copy all available JAR files from modules
COPY --from=builder /build/modules/*/target/*.jar /opt/ignite/libs/
# Copy Maven dependencies (including Spring framework)
COPY --from=builder /build/libs/*.jar /opt/ignite/libs/
# Copy target.jar for security scanning
COPY --from=builder /app/target.jar /app/target.jar

# Copy binary and configuration files
COPY --from=builder /build/bin /opt/ignite/bin
COPY --from=builder /build/config /opt/ignite/config
# Copy licenses and examples if they exist (use RUN to handle missing directories)
RUN mkdir -p /opt/ignite/licenses /opt/ignite/examples && \
    cp -r /build/licenses/* /opt/ignite/licenses/ 2>/dev/null || true && \
    cp -r /build/examples/* /opt/ignite/examples/ 2>/dev/null || true && \
    chmod +x /opt/ignite/bin/*.sh

# Set environment variables
ENV IGNITE_HOME=/opt/ignite
ENV CONFIG=/opt/ignite/config/ignite-rest.xml

# Create work directory
RUN mkdir -p /opt/ignite/work

# Expose Ignite ports
EXPOSE 11211 47100 47500 8080 11080

# Start Ignite
CMD ["/opt/ignite/bin/ignite.sh"]