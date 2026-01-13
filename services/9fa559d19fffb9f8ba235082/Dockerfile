# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

# Create dummy jar files to satisfy system-scoped dependencies
RUN mkdir -p /opt/java/openjdk/lib/ && touch /opt/java/openjdk/lib/jconsole.jar && touch /opt/java/openjdk/lib/tools.jar

WORKDIR /app
COPY JavaSecurity/Apache/Shiro/CVE-2010-3863/pom.xml ./pom.xml
RUN mvn dependency:go-offline -B
COPY JavaSecurity/Apache/Shiro/CVE-2010-3863/src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Create the final image
FROM eclipse-temurin:17-jre-alpine
RUN apk add --no-cache curl mysql-client
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
CMD ["java", "-jar", "app.jar"]
