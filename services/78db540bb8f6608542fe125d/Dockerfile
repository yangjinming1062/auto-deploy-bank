FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY . .
RUN mvn clean install -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/roncoo-pay-web-gateway/target/*.jar app.jar
EXPOSE 8092
CMD ["java", "-jar", "app.jar"]
