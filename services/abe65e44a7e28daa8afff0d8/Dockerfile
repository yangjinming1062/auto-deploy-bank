# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

COPY king-admin-java/pom.xml ./king-admin-java/pom.xml
RUN cd king-admin-java && mvn dependency:go-offline -B

COPY king-admin-java/src ./king-admin-java/src
RUN cd king-admin-java && mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:8-jre-alpine

RUN apk add --no-cache curl

WORKDIR /app

COPY --from=builder /app/king-admin-java/target/king-admin-java-0.0.1-SNAPSHOT.jar target.jar

EXPOSE 8080

CMD ["java", "-jar", "target.jar"]