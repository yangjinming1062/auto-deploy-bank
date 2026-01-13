FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY . .
# First, download dependencies to leverage Docker cache
RUN mvn dependency:go-offline -B -pl example-app -am
# Then, build the application
RUN mvn clean package -pl example-app -am -DskipTests -B

FROM eclipse-temurin:17-jre-alpine
RUN apk add --no-cache curl
WORKDIR /app
COPY --from=builder /app/example-app/target/*.jar app.jar
CMD ["java", "-jar", "app.jar"]
