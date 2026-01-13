# Stage 1: Build the application with Maven
FROM maven:3.8-jdk-8 AS builder
WORKDIR /app
COPY . .
RUN mvn -DskipTests clean install -U

# Stage 2: Create a slim runtime image
FROM adoptopenjdk/openjdk8:alpine-jre
WORKDIR /app
# Copy the application JAR from the builder stage
COPY --from=builder /app/myth-admin/target/myth-admin-2.0.2-RELEASE.jar app.jar
EXPOSE 8888
# Run the application
CMD ["java", "-jar", "app.jar"]