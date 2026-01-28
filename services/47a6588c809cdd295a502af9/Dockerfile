# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy all source code first for proper module resolution
COPY pom.xml ./
COPY eden-agents ./eden-agents
COPY eden-components ./eden-components
COPY eden-plugins ./eden-plugins
COPY eden-tests ./eden-tests

# Build the JAR file (using eden-deployment-test-tomcat as the target application)
# Use Tomcat 9.4.x instead of 10.x for Spring Boot 2.4.x compatibility
RUN printf '%s\n' '<?xml version="1.0" encoding="UTF-8"?>' \
'<project xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
'		 xmlns="http://maven.apache.org/POM/4.0.0"' \
'		 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">' \
'' \
'	<modelVersion>4.0.0</modelVersion>' \
'	<parent>' \
'		<groupId>io.github.shiyindaxiaojie</groupId>' \
'		<artifactId>eden-deployment-tests</artifactId>' \
'		<version>0.0.1-SNAPSHOT</version>' \
'		<relativePath>../pom.xml</relativePath>' \
'	</parent>' \
'	<artifactId>eden-deployment-test-tomcat</artifactId>' \
'	<packaging>jar</packaging>' \
'	<name>eden-deployment-test-tomcat</name>' \
'	<description>Tomcat 部署测试</description>' \
'' \
'	<properties>' \
'		<cargo.container.id>tomcat7x</cargo.container.id>' \
'		<cargo.container.url>' \
'			https://repo1.maven.org/maven2/org/apache/tomcat/tomcat/${tomcat.version}/tomcat-${tomcat.version}.zip' \
'		</cargo.container.url>' \
'		<tomcat.version>9.0.56</tomcat.version>' \
'	</properties>' \
'' \
'	<dependencies>' \
'		<dependency>' \
'			<groupId>org.springframework.boot</groupId>' \
'			<artifactId>spring-boot-starter-web</artifactId>' \
'			<exclusions>' \
'				<exclusion>' \
'					<groupId>org.apache.logging.log4j</groupId>' \
'					<artifactId>log4j-slf4j-impl</artifactId>' \
'				</exclusion>' \
'				<exclusion>' \
'					<groupId>org.apache.logging.log4j</groupId>' \
'					<artifactId>log4j-to-slf4j</artifactId>' \
'				</exclusion>' \
'				<exclusion>' \
'					<groupId>org.slf4j</groupId>' \
'					<artifactId>jcl-over-slf4j</artifactId>' \
'				</exclusion>' \
'				<exclusion>' \
'					<groupId>org.slf4j</groupId>' \
'					<artifactId>jul-to-slf4j</artifactId>' \
'				</exclusion>' \
'			</exclusions>' \
'		</dependency>' \
'	</dependencies>' \
'' \
'	<build>' \
'		<plugins>' \
'			<plugin>' \
'				<groupId>org.springframework.boot</groupId>' \
'				<artifactId>spring-boot-maven-plugin</artifactId>' \
'				<executions>' \
'					<execution>' \
'						<goals>' \
'							<goal>repackage</goal>' \
'						</goals>' \
'					</execution>' \
'				</executions>' \
'			</plugin>' \
'		</plugins>' \
'	</build>' \
'</project>' > eden-tests/eden-deployment-tests/eden-deployment-test-tomcat/pom.xml && \
export MAVEN_OPTS="--add-opens jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.jvm=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED \
--add-opens jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED" && \
mvn clean package -B -DskipTests -pl eden-tests/eden-deployment-tests/eden-deployment-test-tomcat -am

# Stage 2: Runtime with JRE
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/eden-tests/eden-deployment-tests/eden-deployment-test-tomcat/target/eden-deployment-test-tomcat.jar ./app.jar

# Copy to target.jar for security scanning volume mount
COPY --from=builder /app/eden-tests/eden-deployment-tests/eden-deployment-test-tomcat/target/eden-deployment-test-tomcat.jar ./target.jar

# Expose the default port
EXPOSE 8080

# Run the JAR application
CMD ["java", "-jar", "app.jar"]