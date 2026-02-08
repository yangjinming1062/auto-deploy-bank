FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

COPY target.jar target.jar

EXPOSE 8080

ENV PORT=8080
ENV APP_UPDATE_FILE_DIR=/app/uploads
ENV spring.datasource.default=h2

RUN mkdir -p /app/uploads

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

ENTRYPOINT ["java", "-jar", "target.jar"]