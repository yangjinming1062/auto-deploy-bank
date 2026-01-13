# Multi-stage build for DL4J examples
FROM maven:3-eclipse-temurin-17 AS builder

WORKDIR /app/dl4j-examples

# Copy pom.xml first to leverage Docker cache
COPY dl4j-examples/pom.xml pom.xml

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY dl4j-examples/src src
COPY dl4j-examples/src/main/resources src/main/resources

# Build the project
RUN mvn clean package -DskipTests -B

# Copy shaded JAR for volume mounting
RUN cp target/dl4j-examples-*-shaded.jar /tmp/app.jar

# Run the web service
CMD ["sh", "-c", "mvn exec:java -Dexec.mainClass=org.deeplearning4j.examples.webservice.IrisWebService"]