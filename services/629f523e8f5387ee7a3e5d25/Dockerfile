# Stage 1: Builder - Build the JAR with Gradle
FROM gradle:9.1-jdk17 AS builder

WORKDIR /app

COPY build.gradle settings.gradle ./
COPY gradle ./gradle
COPY libs ./libs
COPY src ./src

RUN gradle jar -x test -x spotlessCheck -q

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

RUN apk add --no-cache wget curl

EXPOSE 32349

COPY --from=builder /app/build/libs/PacketProxy.jar app.jar

CMD ["java", "-cp", "app.jar", "packetproxy.HubServerStarter"]
