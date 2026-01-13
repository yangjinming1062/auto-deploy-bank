FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app

# Copy all pom.xml files from the modules
COPY pom.xml .
COPY modules/openapi-generator/pom.xml ./modules/openapi-generator/
COPY modules/openapi-generator-cli/pom.xml ./modules/openapi-generator-cli/
COPY modules/openapi-generator-core/pom.xml ./modules/openapi-generator-core/
COPY modules/openapi-generator-online/pom.xml ./modules/openapi-generator-online/
COPY modules/openapi-generator-maven-plugin/pom.xml ./modules/openapi-generator-maven-plugin/
COPY modules/openapi-generator-gradle-plugin/pom.xml ./modules/openapi-generator-gradle-plugin/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy the rest of the source code
COPY . .

# Build the project
RUN mvn clean install -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/modules/openapi-generator-online/target/openapi-generator-online.jar /app/target.jar
EXPOSE 8080
CMD ["java", "-jar", "/app/target.jar"]
