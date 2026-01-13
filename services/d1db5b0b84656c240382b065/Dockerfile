FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY ./target.jar /app/target.jar
EXPOSE 8081
CMD ["java", "-jar", "/app/target.jar"]
