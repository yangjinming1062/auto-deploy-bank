#
# Copyright © 2019 同程艺龙 (zhihui.li@ly.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy all source files first for Maven multi-module project
COPY pom.xml .
COPY conf ./conf
COPY flower.common ./flower.common
COPY flower.center ./flower.center
COPY flower.sample ./flower.sample
COPY flower.core ./flower.core
COPY flower.web ./flower.web
COPY flower.config ./flower.config
COPY flower.serializer ./flower.serializer
COPY flower.registry ./flower.registry
COPY flower.filter ./flower.filter
COPY flower.container ./flower.container
COPY flower.bom ./flower.bom
COPY flower.test ./flower.test
COPY flower.tools ./flower.tools
COPY flower.boot.starter ./flower.boot.starter
COPY flower.ddd ./flower.ddd

# Create a patched pom.xml for flower.center.impl that uses explicit versions
# This fixes the snakeyaml and logback version conflicts by using Spring Boot 2.1.5 consistently
RUN cat > flower.center/flower.center.impl/pom.xml << 'EOFPOM'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.ly.train</groupId>
        <artifactId>flower.center</artifactId>
        <version>${revision}</version>
    </parent>
    <artifactId>flower.center.impl</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-core</artifactId>
            <version>1.2.13</version>
        </dependency>
        <dependency>
            <groupId>com.ly.train</groupId>
            <artifactId>flower.center.core</artifactId>
            <version>${revision}</version>
        </dependency>
        <dependency>
            <groupId>com.ly.train</groupId>
            <artifactId>flower.web</artifactId>
            <version>${revision}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
            <version>2.1.5.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>2.1.5.RELEASE</version>
        </dependency>
        <!-- Explicitly override snakeyaml to 1.23 (compatible with Spring Boot 2.1.5) -->
        <dependency>
            <groupId>org.yaml</groupId>
            <artifactId>snakeyaml</artifactId>
            <version>1.23</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.1.5.RELEASE</version>
                <configuration>
                    <mainClass>com.ly.train.flower.center.CenterApplication</mainClass>
                </configuration>
                <executions>
                    <execution>
                        <id>package</id>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                        <phase>package</phase>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
EOFPOM

# Build the center module (skip tests)
RUN mvn clean package -DskipTests -B -pl flower.center/flower.center.impl -am

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/flower.center/flower.center.impl/target/flower.center.impl-*.jar app.jar

# Expose default Spring Boot port (8080)
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]