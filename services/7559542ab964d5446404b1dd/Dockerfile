FROM eclipse-temurin:17-jdk-alpine AS builder
WORKDIR /app
COPY . .
RUN chmod +x gradlew && ./gradlew assemble -x test --no-daemon

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
# Copy the example JAR
COPY --from=builder /app/servicetalk-examples/http/helloworld/build/libs/servicetalk-examples-http-helloworld-*.jar app.jar
COPY --from=builder /app/servicetalk-examples/http/helloworld/build/libs/servicetalk-examples-http-helloworld-*.jar target.jar
# Copy all project JARs
COPY --from=builder /app/*/build/libs/*.jar /app/lib/
# Copy external dependencies from Gradle cache - keep all jars including slf4j
COPY --from=builder /root/.gradle/caches/modules-2/files-2.1 /tmp/gradle-cache
RUN find /tmp/gradle-cache -name "*.jar" -type f -exec cp {} /app/lib/ \; 2>/dev/null && rm -rf /tmp/gradle-cache
# Only remove log4j-2.24 jars that conflict with 2.23 and opentracing-log4j2 which conflicts with log4j2-mdc
RUN rm -f /app/lib/*log4j*2.24*.jar /app/lib/*opentracing-log4j2*.jar 2>/dev/null || true
# Create minimal log4j2 config without lookups
RUN echo '<?xml version="1.0" encoding="UTF-8"?><Configuration status="info"><Appenders><Console name="Console" target="SYSTEM_OUT"><PatternLayout pattern="%d %30t [%-5level] %-30logger{1} - %msg%n"/></Console></Appenders><Loggers><Logger name="io.servicetalk.http.netty.NettyHttpServer" level="DEBUG"/><Logger name="io.servicetalk.concurrent.api" level="DEBUG"/><Root level="INFO"><AppenderRef ref="Console"/></Root></Loggers></Configuration>' > /app/log4j2.xml
EXPOSE 8080
CMD ["/bin/sh", "-c", "java -Dlog4j.configurationFile=/app/log4j2.xml -Dlog4j2.threadContextMap=io.servicetalk.log4j2.mdc.DefaultServiceTalkThreadContextMap -cp \"app.jar:lib/*\" io.servicetalk.examples.http.helloworld.async.HelloWorldServer"]