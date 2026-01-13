# Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

ENV GEN_DIR /opt/openapi-generator
WORKDIR ${GEN_DIR}

# Required from a licensing standpoint
COPY ./LICENSE ${GEN_DIR}

# Required to compile openapi-generator
COPY ./google_checkstyle.xml ${GEN_DIR}

# Copy all pom.xml files for dependency caching
COPY ./pom.xml ${GEN_DIR}
COPY ./modules/openapi-generator/pom.xml ${GEN_DIR}/modules/openapi-generator/
COPY ./modules/openapi-generator-cli/pom.xml ${GEN_DIR}/modules/openapi-generator-cli/
COPY ./modules/openapi-generator-core/pom.xml ${GEN_DIR}/modules/openapi-generator-core/
COPY ./modules/openapi-generator-gradle-plugin/pom.xml ${GEN_DIR}/modules/openapi-generator-gradle-plugin/
COPY ./modules/openapi-generator-maven-plugin/pom.xml ${GEN_DIR}/modules/openapi-generator-maven-plugin/
COPY ./modules/openapi-generator-online/pom.xml ${GEN_DIR}/modules/openapi-generator-online/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY ./modules/openapi-generator ${GEN_DIR}/modules/openapi-generator
COPY ./modules/openapi-generator-cli ${GEN_DIR}/modules/openapi-generator-cli
COPY ./modules/openapi-generator-core ${GEN_DIR}/modules/openapi-generator-core
COPY ./modules/openapi-generator-gradle-plugin ${GEN_DIR}/modules/openapi-generator-gradle-plugin
COPY ./modules/openapi-generator-maven-plugin ${GEN_DIR}/modules/openapi-generator-maven-plugin
COPY ./modules/openapi-generator-online ${GEN_DIR}/modules/openapi-generator-online

# Build the online module
RUN mvn clean package -DskipTests -B -pl modules/openapi-generator-online -am

# Runtime stage
FROM eclipse-temurin:17-jdk-alpine

ENV GEN_DIR /opt/openapi-generator
WORKDIR ${GEN_DIR}

# Copy JAR from builder stage
COPY --from=builder ${GEN_DIR}/modules/openapi-generator-online/target/openapi-generator-online.jar app.jar

# Copy entrypoint script
COPY docker-entrypoint-online.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint-online.sh

# Expose port
EXPOSE 8080

# Use entrypoint script
ENTRYPOINT ["/usr/local/bin/docker-entrypoint-online.sh"]
