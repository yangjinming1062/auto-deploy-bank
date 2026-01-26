# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy parent pom.xml
COPY pom.xml ./

# Copy module directories
COPY kaifangqian-core ./kaifangqian-core
COPY kaifangqian-system ./kaifangqian-system
COPY kaifangqian-tools ./kaifangqian-tools

# Build the project (multi-module build from parent)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

RUN mkdir /usr/share/fonts/chinese -p
COPY file/simsun.ttc /usr/share/fonts/chinese
COPY file/simkai.ttf /usr/share/fonts/chinese
COPY file/simhei.ttf /usr/share/fonts/chinese
COPY file/simfang.ttf /usr/share/fonts/chinese

# Refresh font cache
RUN fc-cache -fv && fc-list : family

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# Copy file directory
COPY file /home/kaifangqian/file

# Copy the built JAR from builder stage
# The JAR is in kaifangqian-system/target/kaifangqian.jar
COPY --from=builder /app/kaifangqian-system/target/kaifangqian.jar app.jar

# Volume mount for security scanning
VOLUME ["/app/target.jar"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8899/resrun-paas/actuator/health || exit 1

ENTRYPOINT ["sh", "-c", "exec java -jar -Dspring.profiles.active=prod -Dproject.name=kaifangqian app.jar"]