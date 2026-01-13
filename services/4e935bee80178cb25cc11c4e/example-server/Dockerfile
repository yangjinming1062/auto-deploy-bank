FROM maven:3.9-eclipse-temurin-8 as builder
WORKDIR /app
COPY pom.xml .
COPY rpc-framework-common/pom.xml rpc-framework-common/
COPY hello-service-api/pom.xml hello-service-api/
COPY rpc-framework-simple/pom.xml rpc-framework-simple/
COPY example-client/pom.xml example-client/
COPY example-server/pom.xml example-server/
COPY rpc-framework-common/src rpc-framework-common/src
COPY hello-service-api/src hello-service-api/src
COPY rpc-framework-simple/src rpc-framework-simple/src
COPY example-client/src example-client/src
COPY example-server/src example-server/src
RUN mvn clean package -DskipTests -B
FROM maven:3.9-eclipse-temurin-8
# Install netcat for health checks
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
WORKDIR /app
# Create target directory
RUN mkdir -p /app/target
# Copy JAR to both app.jar (for running) and target.jar (for volume mount)
COPY --from=builder /app/example-server/target/example-server-1.0-SNAPSHOT.jar app.jar
COPY --from=builder /app/example-server/target/example-server-1.0-SNAPSHOT.jar target.jar
EXPOSE 9998
ENTRYPOINT ["java", "-jar", "app.jar"]
