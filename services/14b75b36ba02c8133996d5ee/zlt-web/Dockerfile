FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy pre-built JAR file
COPY layui-web.jar app.jar

EXPOSE 8066

CMD ["java", "-XX:+IgnoreUnrecognizedVMOptions", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
