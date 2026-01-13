FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY courses/java-microservices/spring-cloud-gcp-guestbook/1-bootstrap/guestbook-service/pom.xml .
COPY courses/java-microservices/spring-cloud-gcp-guestbook/1-bootstrap/guestbook-service/src ./src
RUN mvn dependency:go-offline -B
RUN mvn clean package -DskipTests -B

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/guestbook-0.0.1-SNAPSHOT.jar /app/target.jar
EXPOSE 8081
CMD ["java", "-jar", "/app/target.jar"]
