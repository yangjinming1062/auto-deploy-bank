# Lightweight runtime stage using pre-built JAR
FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy the pre-built JAR file
COPY target/ruoyi-admin.jar target.jar

# Expose the application port
EXPOSE 6039

# Run the application
CMD ["java", "-jar", "target.jar"]