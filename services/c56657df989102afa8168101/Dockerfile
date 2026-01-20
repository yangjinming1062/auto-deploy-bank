#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy source code first (includes pom.xml and all modules)
COPY . .

# Build the project (skip tests, use CI profile)
RUN mvn clean package -DskipTests -Pci -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install zip for modifying JAR files (JARs are ZIP format)
RUN apk add --no-cache zip

ENV TZ=Asia/Shanghai
ENV SEATUNNEL_WEB_HOME=/opt/app/seatunnel-web
ENV DOCKER=true

# Set SEATUNNEL_HOME to the libs directory where connectors are loaded from
ENV SEATUNNEL_HOME=/opt/app/seatunnel-web

WORKDIR $SEATUNNEL_WEB_HOME

# Create necessary directories
RUN mkdir -p $SEATUNNEL_WEB_HOME/libs \
             $SEATUNNEL_WEB_HOME/datasource \
             $SEATUNNEL_WEB_HOME/conf \
             $SEATUNNEL_WEB_HOME/logs \
             $SEATUNNEL_WEB_HOME/bin

# Copy the built JAR file from builder stage
# The main application JAR is in seatunnel-server/seatunnel-app/target/
COPY --from=builder /build/seatunnel-server/seatunnel-app/target/*.jar app.jar

# Copy libraries and datasource plugins from the distribution (nested structure)
COPY --from=builder /build/seatunnel-web-dist/target/apache-seatunnel-web-1.0.3-SNAPSHOT/apache-seatunnel-web-1.0.3-SNAPSHOT/libs/ $SEATUNNEL_WEB_HOME/libs/
COPY --from=builder /build/seatunnel-web-dist/target/apache-seatunnel-web-1.0.3-SNAPSHOT/apache-seatunnel-web-1.0.3-SNAPSHOT/datasource/ $SEATUNNEL_WEB_HOME/datasource/

# Remove hazelcast-client.yaml and hazelcast.yaml from seatunnel-engine-common JAR
# These files contain hardcoded ports 5801-5815 that would cause connection failures
# Using zip since JAR files are in ZIP format
RUN for jar in $SEATUNNEL_WEB_HOME/libs/seatunnel-engine-common-*.jar; do \
      if [ -f "$jar" ] && zip -l "$jar" 2>/dev/null | grep -q "hazelcast-client.yaml"; then \
        zip -d "$jar" "hazelcast-client.yaml" 2>/dev/null || true; \
      fi; \
      if [ -f "$jar" ] && zip -l "$jar" 2>/dev/null | grep -q "hazelcast.yaml"; then \
        zip -d "$jar" "hazelcast.yaml" 2>/dev/null || true; \
      fi; \
    done

# Copy configuration files
COPY --from=builder /build/seatunnel-server/seatunnel-app/src/main/resources/*.yml $SEATUNNEL_WEB_HOME/conf/
COPY --from=builder /build/seatunnel-server/seatunnel-app/src/main/resources/*.yaml $SEATUNNEL_WEB_HOME/conf/
COPY --from=builder /build/seatunnel-server/seatunnel-app/src/main/resources/*.xml $SEATUNNEL_WEB_HOME/conf/
COPY --from=builder /build/seatunnel-server/seatunnel-app/src/main/bin/*.sh $SEATUNNEL_WEB_HOME/bin/
RUN chmod +x $SEATUNNEL_WEB_HOME/bin/*.sh

# Copy UI static files
COPY --from=builder /build/seatunnel-ui/dist/ $SEATUNNEL_WEB_HOME/ui/

# Copy script directory for H2 database initialization
COPY --from=builder /build/seatunnel-server/seatunnel-app/src/main/resources/script $SEATUNNEL_WEB_HOME/script

# Expose the application port
EXPOSE 8801

# Run the application directly with java -cp (H2 profile for testing)
# Disable Hazelcast auto-configuration to prevent connection attempts
CMD ["java", "-server", "-Xms1g", "-Xmx1g", "-Xmn512m", \
     "-cp", "conf:libs/*:datasource/*", \
     "org.apache.seatunnel.app.SeatunnelApplication", \
     "--spring.profiles.active=h2", \
     "--spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.hazelcast.HazelcastClientAutoConfiguration", \
     "--spring.config.name=application.yml", \
     "--spring.config.location=classpath:application.yml,file:./conf/"]