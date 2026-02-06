# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy project files
COPY pom.xml .
COPY server ./server
COPY core ./core
COPY morphology ./morphology
COPY tokenization ./tokenization
COPY lm ./lm
COPY all ./all
COPY experiment ./experiment
COPY lang-id ./lang-id
COPY grpc ./grpc
COPY normalization ./normalization
COPY examples ./examples
COPY ner ./ner
COPY apps ./apps
COPY classification ./classification

# Uncomment the server module in pom.xml to enable building
RUN sed -i 's/<!-- disable server modules for the time being.-->//g' pom.xml && \
    sed -i 's/<!--<module>server<\/module>-->/<module>server<\/module>/g' pom.xml

# Fix the server module's parent version to match root pom.xml (0.17.2)
# Also fix the server's own version
RUN sed -i 's/<version>0\.1\.0<\/version>/<version>0.17.2<\/version>/g' server/pom.xml && \
    sed -i 's/<version>0\.16\.0<\/version>/<version>0.17.2<\/version>/g' server/pom.xml

# Add spring-boot-maven-plugin configuration for repackaging
RUN sed -i '/<artifactId>spring-boot-maven-plugin<\/artifactId>/a\        <configuration>\n          <executable>true</executable>\n        </configuration>' server/pom.xml

# Build dependencies first (without server module)
RUN mvn clean install -DskipTests -B -pl '!server'

# Build server module with repackaging to create executable JAR
RUN cd server && mvn clean package spring-boot:repackage -DskipTests -B

# Stage 2: Runtime stage
FROM amazoncorretto:17-alpine

WORKDIR /app

# Copy the built JAR to internal location (will be copied to bind mount at runtime)
COPY --from=builder /app/server/target/zemberek-server-0.17.2.jar /app/built/target.jar

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the Spring Boot port (default 8080)
EXPOSE 8080

# Run the application via entrypoint script
ENTRYPOINT ["/entrypoint.sh"]