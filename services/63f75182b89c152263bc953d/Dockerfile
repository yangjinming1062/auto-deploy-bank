# Stage 1: Builder
FROM eclipse-temurin:17-jdk AS builder

# Install bash for gradlew
RUN apt-get update && apt-get install -y --no-install-recommends bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy gradle wrapper and build files first for better caching
COPY gradlew ./
COPY gradle/ ./gradle/
COPY versions.gradle ./
COPY versions.properties ./
COPY gradle.properties ./
COPY settings.gradle /tmp/
COPY build.gradle /tmp/

# Create minimal build.gradle and settings.gradle for the container
# Remove asciidoctor-related plugins and problematic subprojects that spring-boot-example doesn't need
RUN cat /tmp/build.gradle | grep -v 'asciidoctor-gradle-plugin' | grep -v 'asciidoctorj-pdf' > build.gradle && \
    rm /tmp/build.gradle && \
    cat /tmp/settings.gradle | grep -v 'crnk-documentation' | grep -v 'crnk-gen' | grep -v 'crnk-bom' > settings.gradle && \
    rm /tmp/settings.gradle

# Copy all subprojects needed for the build
COPY crnk-core ./crnk-core
COPY crnk-reactive ./crnk-reactive
COPY crnk-home ./crnk-home
COPY crnk-validation ./crnk-validation
COPY crnk-ui ./crnk-ui
COPY crnk-operations ./crnk-operations
COPY crnk-security ./crnk-security
COPY crnk-test ./crnk-test
COPY crnk-testkit ./crnk-testkit
COPY crnk-client ./crnk-client
COPY crnk-meta ./crnk-meta

COPY crnk-monitor ./crnk-monitor
COPY crnk-setup ./crnk-setup
COPY crnk-data ./crnk-data
COPY crnk-format ./crnk-format

COPY crnk-integration-examples/spring-boot-example ./crnk-integration-examples/spring-boot-example

# Modify spring-boot-example build.gradle to not require crnk-gen-java and add manifest Main-Class
RUN sed -i "/compileOnly project(':crnk-gen:crnk-gen-java')/d" crnk-integration-examples/spring-boot-example/build.gradle && \
    sed -i "/annotationProcessor project(':crnk-gen:crnk-gen-java')/d" crnk-integration-examples/spring-boot-example/build.gradle && \
    echo "" >> crnk-integration-examples/spring-boot-example/build.gradle && \
    echo "jar { manifest { attributes 'Main-Class': 'io.crnk.example.springboot.SpringBootExampleApplication' } }" >> crnk-integration-examples/spring-boot-example/build.gradle

# Download dependencies and build the project
# Create init script to add repositories for buildscript dependencies (grolifant is in JCenter)
RUN mkdir -p ~/.gradle && \
    echo 'allprojects { buildscript { repositories { mavenCentral(); gradlePluginPortal(); maven { url "https://jcenter.bintray.com" } } } }' > ~/.gradle/init.gradle && \
    chmod +x gradlew && \
    ./gradlew :crnk-integration-examples:spring-boot-example:clean :crnk-integration-examples:spring-boot-example:installDist --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:17-jre

WORKDIR /app

# Create non-root user for security
RUN groupadd --system app && useradd --system --gid app app

# Copy the distribution from builder stage
COPY --from=builder /app/crnk-integration-examples/spring-boot-example/build/install/spring-boot-example/ .

# Add JVM options for Spring Boot 2.x compatibility with Java 17
ENV JAVA_OPTS="--add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.reflect=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED"

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the default Spring Boot port
EXPOSE 8080

# Run the application using the distribution scripts
CMD ["bin/spring-boot-example"]