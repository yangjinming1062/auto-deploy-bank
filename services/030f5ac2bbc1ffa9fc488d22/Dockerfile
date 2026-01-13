# Simple Dockerfile for Wire gRPC sample server
FROM amazoncorretto:17

WORKDIR /app

# Copy the entire installation distribution
COPY samples/wire-grpc-sample/server/build/install/server/ .

# Expose the web server port
EXPOSE 8080

# Set environment variables
ENV DEPLOYMENT=testing
ENV GRADLE_OPTS=-Dorg.gradle.jvmargs=-Xmx4g -Dorg.gradle.daemon=false -Dkotlin.incremental=false

# Run the application using the startup script
CMD ["bin/server"]
