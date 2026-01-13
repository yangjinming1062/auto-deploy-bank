FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src src
RUN mvn clean package -DskipTests -B -Dcheckstyle.skip=true

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/keycloak-config-cli-*.jar target.jar
RUN apk add --no-cache python3 py3-pip
COPY --from=builder /app/target/keycloak-config-cli-*.jar /app/target.jar
COPY index.html /app/index.html
EXPOSE 40013
CMD ["sh", "-c", "python3 -m http.server 40013 --bind 0.0.0.0"]
