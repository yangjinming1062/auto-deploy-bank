# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy entire project structure
COPY . .

# Create stub for missing ipdatabase dependency
RUN mkdir -p /tmp/stub/src/main/java/com/ggstar/util/ip && \
    echo '<?xml version="1.0" encoding="UTF-8"?><project><modelVersion>4.0.0</modelVersion><groupId>com.ggstar</groupId><artifactId>ipdatabase</artifactId><version>1.0-SNAPSHOT</version><packaging>jar</packaging></project>' > /tmp/stub/pom.xml && \
    echo 'package com.ggstar.util.ip; public class IpHelper { public static String findRegionByIp(String ip) { return "Unknown"; } }' > /tmp/stub/src/main/java/com/ggstar/util/ip/IpHelper.java && \
    cd /tmp/stub && \
    mvn compile jar:jar install:install -DskipTests -B

# First install zx-bt-top pom to local repository (required because parent pom imports it as BOM)
# Use -f to specify the pom file directly, avoiding reading the parent pom.xml
RUN cd zx-bt-top && mvn install:install-file -Dfile=pom.xml -DgroupId=com.zx.bt -DartifactId=zx-bt-top -Dversion=1.0 -Dpackaging=pom -B

# Now install parent pom and build modules
# zx-bt-common must be built and installed first as zx-bt-web depends on it
# Use maven-shade-plugin to create uber jar with all dependencies bundled
RUN sed -i '/<execution>/,/<\/execution>/d' zx-bt-web/pom.xml && \
    sed -i '/<plugins>/a\            <plugin>\n                <groupId>org.apache.maven.plugins</groupId>\n                <artifactId>maven-shade-plugin</artifactId>\n                <version>3.5.1</version>\n                <executions>\n                    <execution>\n                        <phase>package</phase>\n                        <goals><goal>shade</goal></goals>\n                        <configuration>\n                            <transformers>\n                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">\n                                    <mainClass>com.zx.bt.web.WebApplication</mainClass>\n                                </transformer>\n                                <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>\n                                <transformer implementation="org.apache.maven.plugins.shade.resource.AppendingTransformer">\n                                    <resource>META-INF/spring.factories</resource>\n                                </transformer>\n                            </transformers>\n                        </configuration>\n                    </execution>\n                </executions>\n            </plugin>' zx-bt-web/pom.xml && \
    mvn install -N -B && \
    mvn clean install -DskipTests -B -f zx-bt-common/pom.xml && \
    mvn clean package -DskipTests -B -f zx-bt-web/pom.xml && \
    mv zx-bt-web/target/zx-bt-web.jar zx-bt-web/target/app.jar

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
# Copy to scanning directory for entrypoint script to use
COPY --from=builder /app/zx-bt-web/target/app.jar /scanning/app.jar

# Expose the application port
EXPOSE 8081

# Create a startup script that copies JAR to mounted volume and runs the app
RUN printf '#!/bin/sh\ncp /scanning/app.jar /app/target.jar\nexec java -jar /scanning/app.jar\n' > /entrypoint.sh && chmod +x /entrypoint.sh

CMD ["/bin/sh", "/entrypoint.sh"]