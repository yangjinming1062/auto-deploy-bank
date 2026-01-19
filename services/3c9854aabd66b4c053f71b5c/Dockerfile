# Stage 1: Build the application using Gradle
FROM gradle:8.11.1-jdk21 AS builder

WORKDIR /build

# Copy gradle wrapper and build files
COPY gradle gradle
COPY gradlew .
COPY settings.gradle .
COPY build.gradle .
COPY platform platform
COPY cli cli
COPY core core
COPY script script
COPY executor executor
COPY scheduler scheduler
COPY webserver webserver
COPY worker worker
COPY jdbc jdbc
COPY jdbc-h2 jdbc-h2
COPY jdbc-mysql jdbc-mysql
COPY jdbc-postgres jdbc-postgres
COPY storage-local storage-local
COPY repository-memory repository-memory
COPY runner-memory runner-memory
COPY model model
COPY ui ui
COPY tests tests

# Make gradlew executable
RUN chmod +x gradlew

# Initialize git for build
RUN git init && \
    git config user.email "build@kestra.io" && \
    git config user.name "Kestra Builder" && \
    git add . && \
    git commit -m "Initial commit" || true

# Build distribution and shadow JAR
RUN ./gradlew installDist shadowJar --no-daemon

# Create service JAR using gradle container
RUN mkdir -p /tmp/services-src/META-INF/services && \
    echo "io.kestra.storage.local.LocalStorage" > /tmp/services-src/META-INF/services/io.kestra.core.models.Plugin && \
    cd /tmp/services-src && \
    jar -cf /build/build/install/kestra/lib/kestra-services.jar META-INF && \
    rm -rf /tmp/services-src

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

RUN groupadd kestra && \
    useradd -m -g kestra kestra && \
    mkdir -p /app/storage /app/logs /app/local/plugins && \
    chown -R kestra:kestra /app

# Copy all dependencies from distribution
COPY --from=builder --chown=kestra:kestra /build/build/install/kestra/lib/*.jar /app/lib/
COPY --from=builder --chown=kestra:kestra /build/build/install/kestra/bin/* /app/bin/

# Copy shadow JAR for security scanning (will be extracted to host after build)
COPY --from=builder /build/build/libs/kestra.jar /app/target.jar
COPY --from=builder /build/build/libs/kestra.jar /app/target.jar.backup

# Set up classpath and environment
ENV CLASSPATH="/app/lib/*"
ENV JAVA_OPTS="-Xms512m -Xmx2g -Dkestra.repository.type=postgres -Dkestra.queue.type=postgres -Dkestra.storage.type=local -Dkestra.storage.local.basePath=/app/storage"
ENV KESTRA_JAVA_OPTS="-Xms512m -Xmx2g"

# Make scripts executable
RUN chmod +x /app/bin/*

USER kestra

# Run the application using classpath
CMD ["sh", "-c", "java $JAVA_OPTS -cp \"/app/lib/*\" io.kestra.cli.App server standalone"]