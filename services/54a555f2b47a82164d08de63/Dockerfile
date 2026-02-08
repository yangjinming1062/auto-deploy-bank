# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Install protobuf compiler and make (required for building)
RUN apt-get update && apt-get install -y protobuf-compiler make && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pom.xml.in Makefile ./
COPY third_party third_party/
COPY protobuf protobuf/
COPY src src/
COPY test test/
COPY asynchbase.conf ./
COPY .mvn-compat .mvn-compat/
COPY logback.xml ./

# Create symlink for the .mvn-compat path resolution
# Source files are at /app/src/*.java (package org.hbase.async)
# Maven sourceDirectory is .mvn-compat/src/main/java, symlink java folder to src
RUN rm -rf /app/.mvn-compat/src/main/java && \
    ln -s /app/src /app/.mvn-compat/src/main/java

# Generate pom.xml from pom.xml.in
RUN make pom.xml

# Remove parent tag (causes GPG signing issues)
RUN sed -i '/<parent>/,/<\/parent>/d' pom.xml

# Update protobuf version in dependency section
RUN sed -i 's/@PROTOBUF_VERSION@/3.21.12/g' pom.xml && \
    sed -i 's/<version>2\.5\.0<\/version>/<version>3.21.12<\/version>/g' pom.xml

# Update Java source/target to 1.8 and remove Xlint
RUN sed -i 's/<source>1\.6<\/source>/<source>1.8<\/source>/g' pom.xml && \
    sed -i 's/<target>1\.6<\/target>/<target>1.8<\/target>/g' pom.xml && \
    sed -i '/<compilerArgument>-Xlint<\/compilerArgument>/d' pom.xml

# Skip GPG signing
RUN sed -i '/<artifactId>maven-gpg-plugin<\/artifactId>/a\          <configuration>\n          <skip>true<\/skip>\n        </configuration>' pom.xml

# Change logback scope from test to runtime
RUN sed -i '/<artifactId>logback-core<\/artifactId>/,/<\/dependency>/ s/<scope>test<\/scope>/<scope>runtime<\/scope>/' pom.xml
RUN sed -i '/<artifactId>logback-classic<\/artifactId>/,/<\/dependency>/ s/<scope>test<\/scope>/<scope>runtime<\/scope>/' pom.xml

# Fix compiler plugin to ignore warnings
RUN sed -i '/<artifactId>maven-compiler-plugin<\/artifactId>/,/<\/plugin>/ s/<configuration>/<configuration>\n          <fork>true<\/fork>\n          <compilerArgs>\n            <arg>-Xlint:none<\/arg>\n          <\/compilerArgs>/' pom.xml

# Find the closing </plugins> tag and insert maven-shade-plugin before it
RUN sed -i 's|</plugins>|      <plugin>\n        <groupId>org.apache.maven.plugins</groupId>\n        <artifactId>maven-shade-plugin</artifactId>\n        <version>3.5.1</version>\n        <executions>\n          <execution>\n            <phase>package</phase>\n            <goals>\n              <goal>shade</goal>\n            </goals>\n            <configuration>\n              <transformers>\n                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">\n                  <mainClass>org.hbase.async.App</mainClass>\n                </transformer>\n                <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>\n              </transformers>\n              <filters>\n                <filter>\n                  <artifact>*:*</artifact>\n                  <excludes>\n                    <exclude>META-INF/*.SF</exclude>\n                    <exclude>META-INF/*.DSA</exclude>\n                    <exclude>META-INF/*.RSA</exclude>\n                  </excludes>\n                </filter>\n              </filters>\n              <outputFile>target.jar</outputFile>\n            </configuration>\n          </execution>\n        </executions>\n      </plugin>\n    </plugins>|' pom.xml

# Build the fat JAR (skip test compilation and javadoc)
RUN mvn clean package -Dmaven.test.skip=true -Dmaven.javadoc.skip=true -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /home/application

# Copy the built JAR from builder stage
COPY --from=builder /app/target.jar app.jar

# Copy configuration files
COPY asynchbase.conf /home/application/
COPY logback.xml /home/application/

# Expose the service port
EXPOSE 44112

# Set environment variables for HBase connection
ENV HBASE_ZOOKEEPER_QUORUM=zookeeper
ENV HBASE_ZOOKEEPER_ZNODE_PARENT=/hbase

# Run the application
CMD ["java", "-jar", "app.jar"]