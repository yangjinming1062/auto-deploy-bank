# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

LABEL maintainer="AntonyCheng"

ENV PARAMS=""
ENV TZ=PRC
ENV APP_HOME=/opt/spring-boot-init-template

# Install curl for healthcheck
RUN apk add --no-cache curl

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR $APP_HOME

# Copy built jar from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Create symbolic link for security scanning (maps to the jar file)
RUN ln -sf app.jar target.jar

VOLUME ["$APP_HOME"]

EXPOSE 38080

CMD ["java", "-jar", "app.jar"]