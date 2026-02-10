# Stage 1: Builder
FROM eclipse-temurin:17-jdk AS builder

# Install SBT
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg && \
    echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list && \
    echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list && \
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add - && \
    apt-get update && \
    apt-get install -y sbt && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Build the project using SBT
# Note: This is a library project - compiles classes and creates a basic jar
# Disable OSGi bundle creation which causes version format issues
RUN sbt -Dsbt.log.noformat=true -Dsbt.osgi.skip=true compile

# Create a proper JAR with the compiled classes
# Use msgpack-core classes as the main artifact
WORKDIR /app/msgpack-core
RUN jar cf /app/target.jar -C target/classes .
WORKDIR /app

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the compiled classes for the HTTP server
COPY --from=builder /app/msgpack-core/target/classes /app/classes

# Run the HTTP server with JDK 17+ compatibility flags
CMD ["java", "--add-opens=java.base/java.nio=ALL-UNNAMED", "-cp", "/app/classes", "org.msgpack.core.Server"]