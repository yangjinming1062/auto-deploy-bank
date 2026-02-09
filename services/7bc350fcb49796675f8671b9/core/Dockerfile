# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy and build the models dependency first
COPY models/pom.xml ./models/pom.xml
COPY models/src ./models/src
WORKDIR /app/models

# Patch the pom.xml to override parent Java 6 configuration with Java 11
RUN sed -i '/<\/plugins>/i\
      <plugin>\
        <groupId>org.apache.maven.plugins</groupId>\
        <artifactId>maven-compiler-plugin</artifactId>\
        <version>3.11.0</version>\
        <configuration>\
          <source>11</source>\
          <target>11</target>\
        </configuration>\
      </plugin>' pom.xml && \
    mvn clean install -DskipTests -B -Dmaven.javadoc.skip=true

# Build the core module
WORKDIR /app
COPY core/pom.xml ./core/pom.xml
COPY core/src ./core/src
WORKDIR /app/core

# Patch the pom.xml to override parent Java 6 configuration with Java 11
RUN sed -i '/<\/plugins>/i\
      <plugin>\
        <groupId>org.apache.maven.plugins</groupId>\
        <artifactId>maven-compiler-plugin</artifactId>\
        <version>3.11.0</version>\
        <configuration>\
          <source>11</source>\
          <target>11</target>\
        </configuration>\
      </plugin>' pom.xml && \
    mvn clean compile assembly:single -DskipTests -B -Dmaven.javadoc.skip=true && \
    ls -la /app/core/target/

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built jar from builder stage
COPY --from=builder /app/core/target/reverb-core-*-jar-with-dependencies.jar target.jar

# Expose the HTTP port
EXPOSE 42122

# Run the application
CMD ["java", "-jar", "target.jar"]