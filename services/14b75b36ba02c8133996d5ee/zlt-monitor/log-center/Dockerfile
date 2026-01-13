FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy pre-built JAR file
COPY log-center.jar app.jar

EXPOSE 7200

CMD ["java", "-XX:+IgnoreUnrecognizedVMOptions", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
