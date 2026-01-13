# Stage 1: Build the application using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app

# Copy the pom files and download dependencies to leverage Docker's layer cache
COPY pom.xml .
COPY cachecloud-web/pom.xml ./cachecloud-web/
COPY cachecloud-custom/pom.xml ./cachecloud-custom/
RUN mvn dependency:go-offline -B

# Copy the rest of the application source code
COPY . .

# Compile the application and package it as a WAR file, skipping tests
RUN mvn clean install -DskipTests -B

# Stage 2: Create the final, lightweight runtime image
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

RUN apk --no-cache add curl

RUN mkdir -p /opt/ssh && touch /opt/ssh/id_rsa

# Copy the built WAR file from the builder stage and rename it
COPY --from=builder /app/cachecloud-web/target/cachecloud-web.war app.war

# Expose the port the application will run on
EXPOSE 8080

# Set the command to run the application
CMD ["java", "-jar", "app.war"]
